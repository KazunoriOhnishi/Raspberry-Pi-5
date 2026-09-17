import cv2
from ultralytics import YOLO

def main():
    # 1. YOLOv8のモデルを読み込む
    model = YOLO("yolov8n.pt")

    # 2. 認識させたい元画像ファイルを読み込む
    # ※同じフォルダにある「input.jpg」を読み込む例です
    input_path = "input.png"
    frame = cv2.imread(input_path)

    if frame is None:
        print(f"エラー: 画像ファイル '{input_path}' が見つからないか、読み込めません。")
        return

    # 3. YOLOv8で物体認識を実行
    results = model(frame)

    # 4. 認識結果（枠やラベル）を描画した画像を取得
    for result in results:
        annotated_frame = result.plot()

    # 5. 認識結果の画像を別の名前で保存する
    output_path = "output_result.png"
    cv2.imwrite(output_path, annotated_frame)

    print(f"認識が完了しました！ 結果を '{output_path}' として保存しました。")

if __name__ == "__main__":
    main()
