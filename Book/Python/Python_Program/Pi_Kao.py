# Pi_Kao.py

import cv2  # OpenCVライブラリをインポート（画像処理用）
from libcamera import controls  # libcameraの設定値（コントロール）をインポート
from picamera2 import Picamera2  # Raspberry Pi公式のカメラ制御ライブラリをインポート

# --- 1. 顔検出の準備 ---
# 人間の顔の特徴が記録された「学習済みモデルファイル（XML）」の保存場所を指定
HAAR_FILE = (
    "/usr/share/opencv4/haarcascades/" "haarcascade_frontalface_default.xml"
)
# 指定したファイルを読み込んで、顔検出用のオブジェクト（分類器）を作成
face_detector = cv2.CascadeClassifier(HAAR_FILE)

# OpenCVのウィンドウ表示処理を安定させるためのバックグラウンド処理を開始
cv2.startWindowThread()

# --- 2. カメラの初期設定と開始 ---
picam2 = Picamera2()  # カメラを操作するためのインスタンスを作成

# カメラの基本設定（フォーマットをXRGB8888、画面サイズを横640ピクセル×縦480ピクセルに設定）
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "XRGB8888", "size": (640, 480)}
    )
)
picam2.start()  # カメラによる映像のキャプチャ（取り込み）を開始

# カメラを「連続オートフォーカスモード（被写体に自動でピントを合わせ続ける設定）」にする
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# --- 3. リアルタイム画像処理のメインループ ---
while True:
    # カメラから現在の最新の1フレーム（画像データ）を多次元配列（NumPy配列）として取得
    im = picam2.capture_array()

    # カラー画像をグレー（白黒・グレースケール）画像に変換（顔検出の処理を高速化する）
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # 【顔検出を実行】顔を探し、見つかった全ての顔の位置情報を「faces」に保存
    # ※1.1は画像の縮小率、5は検出の正確さを表すパラメーター
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    # 検出された顔の数だけ、処理を繰り返す（x:左端座標, y:上端座標, w:横幅, h:縦幅）
    for x, y, w, h in faces:
        # 元のカラー画像（im）の顔がある場所に、緑色の四角い枠を描く
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    # 四角枠を描き加えた画像（im）を「Camera」という名前のウィンドウに表示
    cv2.imshow("Camera", im)

    # キーボードからの入力を1ミリ秒間待つ
    key = cv2.waitKey(1)

    # 入力されたキーが「Esc（エスケープ）キー（キーコード: 27）」だった場合
    if key == 27:
        break  # whileによる無限ループを抜ける（プログラムの終了へ）

# --- 4. 後片付け処理 ---
picam2.stop()  # カメラのキャプチャ動作を停止
cv2.destroyAllWindows()  # OpenCVが開いたすべてのウィンドウを閉じる

