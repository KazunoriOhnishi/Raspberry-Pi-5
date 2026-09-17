# camera_infer.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge Impulse .eim モデルを使ったカメラ物体検出プログラム
- 重複するバウンディングボックスをNMS(Non-Maximum Suppression)で除去
- 検出結果をターミナルにテキスト表示
- カメラ映像にバウンディングボックスとラベルを重ねて画面表示

使い方:
    python3 camera_infer.py <modelfile.eim> [camera_id]

例:
    python3 camera_infer.py ./modelfile.eim 0
"""

import cv2
import os
import sys
import time
import signal

from edge_impulse_linux.image import ImageImpulseRunner

# Ctrl+Cで途中終了したときに、後片付け(runner.stop())で使うためグローバル変数にしておく
runner = None

# ==== 調整用パラメータ ====
# この信頼度(0.0〜1.0)未満の検出結果は無視する。誤検出が多い場合は数値を上げる。
CONF_THRESHOLD = 0.6

# 2つの矩形の重なり具合(IoU)がこの値を超えたら「同じ物体の重複検出」とみなして片方を消す。
# 数値を下げるほど、少しの重なりでも積極的に統合される(重複が減りやすい)。
IOU_THRESHOLD = 0.3

# 画面表示だけの拡大率。1.0なら等倍(モデルの入力サイズそのまま、例: 320x320)で表示する。
# 推論(検出の精度)には一切影響しない、見た目だけの設定。
DISPLAY_SCALE = 1.0


def sigint_handler(sig, frame):
    """
    Ctrl+Cが押されたときに呼ばれる処理。
    カメラやモデルのランナーを正しく停止してから終了する。
    """
    print('Interrupted')
    if runner:
        runner.stop()
    sys.exit(0)


# Ctrl+Cのシグナル(SIGINT)を上のsigint_handlerに割り当てる
signal.signal(signal.SIGINT, sigint_handler)


def calc_iou(a, b):
    """
    2つのバウンディングボックス a, b の重なり具合(IoU: Intersection over Union)を計算する。
    IoUは「2つの矩形が重なっている面積」÷「2つの矩形を合わせた面積」で求まる、0〜1の値。
    値が1に近いほどほぼ同じ場所を指しており、0に近いほど重なっていない。
    """
    # 重なっている部分(交差領域)の左上・右下の座標を求める
    x1 = max(a['x'], b['x'])
    y1 = max(a['y'], b['y'])
    x2 = min(a['x'] + a['width'], b['x'] + b['width'])
    y2 = min(a['y'] + a['height'], b['y'] + b['height'])

    # 交差領域の幅・高さ(重なっていない場合は0にする)
    inter_w = max(0, x2 - x1)
    inter_h = max(0, y2 - y1)
    inter_area = inter_w * inter_h

    # それぞれの矩形の面積
    area_a = a['width'] * a['height']
    area_b = b['width'] * b['height']

    # 合計面積(重なり部分を二重に数えないよう引き算する)
    union_area = area_a + area_b - inter_area

    if union_area <= 0:
        return 0
    return inter_area / union_area


def apply_nms(bboxes, conf_threshold, iou_threshold):
    """
    NMS(Non-Maximum Suppression、重複除去)を適用する。
    同じラベルの検出結果同士で大きく重なっているものがあれば、
    信頼度が一番高いものだけを残し、残りは捨てる。

    引数:
        bboxes: モデルが出力した生のバウンディングボックス一覧
        conf_threshold: この信頼度未満は最初から除外する
        iou_threshold: この重なり度合いを超えたら「重複」とみなす

    戻り値:
        重複が取り除かれたバウンディングボックスのリスト
    """
    # まず信頼度でふるい落とす
    boxes = [b for b in bboxes if b['value'] >= conf_threshold]

    # 信頼度が高い順に並び替える(信頼度が高いものを優先して残すため)
    boxes.sort(key=lambda b: b['value'], reverse=True)

    kept = []  # 最終的に残す矩形
    suppressed = [False] * len(boxes)  # すでに「重複」として除外済みかどうかのフラグ

    for i in range(len(boxes)):
        if suppressed[i]:
            continue  # すでに除外済みならスキップ

        # 信頼度が高い方から順に採用していく
        kept.append(boxes[i])

        # 採用した矩形と、同じラベルかつ大きく重なっている残りの矩形を除外する
        for j in range(i + 1, len(boxes)):
            if suppressed[j]:
                continue
            if boxes[i]['label'] == boxes[j]['label'] and \
               calc_iou(boxes[i], boxes[j]) > iou_threshold:
                suppressed[j] = True

    return kept


def draw_boxes(img, boxes):
    """
    画像(img)の上に、バウンディングボックスとラベル(クラス名+信頼度%)を描画する。
    """
    for bb in boxes:
        color = (0, 220, 0)  # 描画色(BGR形式、緑)
        x, y, w, h = bb['x'], bb['y'], bb['width'], bb['height']

        # 矩形を描画(アンチエイリアスありで、線をなめらかにする)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2, cv2.LINE_AA)

        # ラベル文字列を組み立てる(例: "Rimocon 95%"のような表示にする)
        label_text = "%s %.0f%%" % (bb['label'], bb['value'] * 100)

        # 文字列を描画したときの幅・高さを事前に計算する(背景の矩形サイズを決めるため)
        (text_w, text_h), baseline = cv2.getTextSize(
            label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

        # ラベルが画面の外にはみ出さないよう、Y座標を調整
        label_y = max(y, text_h + 4)

        # 文字の後ろに塗りつぶした矩形を描いて、文字を読みやすくする
        cv2.rectangle(img, (x, label_y - text_h - 4),
                      (x + text_w + 4, label_y), color, cv2.FILLED)

        # 白文字でラベルを描画
        cv2.putText(img, label_text, (x + 2, label_y - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    return img


def main(argv):
    global runner

    # 引数チェック(モデルファイルのパスが指定されているか)
    if len(argv) < 1:
        print("使い方: python3 camera_infer.py <modelfile.eim> [camera_id]")
        sys.exit(1)

    model = argv[0]
    # カメラIDが指定されていなければ0番(デフォルトのカメラ)を使う
    camera_id = int(argv[1]) if len(argv) >= 2 else 0

    # モデルファイルへの絶対パスを組み立てる
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    print('MODEL: ' + modelfile)

    # ImageImpulseRunnerでモデルを読み込む(withを使うことで終了時に自動的に後片付けされる)
    with ImageImpulseRunner(modelfile) as runner:
        try:
            # モデルを初期化し、プロジェクト情報などを取得する
            model_info = runner.init()
            print('Loaded runner for "%s / %s"' % (
                model_info['project']['owner'], model_info['project']['name']))

            # 学習時に設定したラベル(クラス名)の一覧を取得
            labels = model_info['model_parameters']['labels']

            # runner.classifier(camera_id) が、カメラのオープン・フレーム取得・推論を
            # まとめて行い、1フレームごとに (推論結果res, 画像img) を返してくれる
            for res, img in runner.classifier(camera_id):

                # 物体検出モデルの場合、結果に"bounding_boxes"キーが含まれる
                if "bounding_boxes" in res["result"].keys():
                    raw_boxes = res["result"]["bounding_boxes"]

                    # NMSで重複するボックスを除去する
                    filtered_boxes = apply_nms(raw_boxes, CONF_THRESHOLD, IOU_THRESHOLD)

                    # ==== テキスト表示(ターミナルへの出力) ====
                    print('Found %d boxes (raw: %d) (%d ms.)' % (
                        len(filtered_boxes), len(raw_boxes),
                        res['timing']['dsp'] + res['timing']['classification']))
                    for bb in filtered_boxes:
                        print('  %s (%.2f): x=%d y=%d w=%d h=%d' % (
                            bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))

                    # ==== 画像への描画 ====
                    img = draw_boxes(img, filtered_boxes)

                # モデル内部の画像はRGB形式なので、OpenCVで表示するためBGR形式に変換する
                display_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                # DISPLAY_SCALEが1.0以外のときだけ、表示用に拡大・縮小する
                if DISPLAY_SCALE != 1.0:
                    display_img = cv2.resize(
                        display_img, None,
                        fx=DISPLAY_SCALE, fy=DISPLAY_SCALE,
                        interpolation=cv2.INTER_LINEAR)

                # ウィンドウに表示
                cv2.imshow('Edge Impulse - Object Detection', display_img)

                # "q"キーが押されたらループを抜けて終了する
                if cv2.waitKey(1) == ord('q'):
                    break

        finally:
            # 正常終了・異常終了どちらの場合でも、カメラとウィンドウを確実に片付ける
            if runner:
                runner.stop()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv[1:])
