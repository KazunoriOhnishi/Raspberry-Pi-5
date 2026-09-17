import cv2
from ultralytics import YOLO

def main():
    # 1. 最も軽量なYOLOv8 Nanoモデルを読み込む（自動でダウンロードされます）
    model = YOLO("yolov8n.pt")

    # 2. USBカメラをオープンする（通常、最初のUSBカメラは '0' になります）
    cap = cv2.VideoCapture(0)

    # カメラが正常に開いたか確認
    if not cap.isOpened():
        print("エラー: USBカメラが見つからないか、開けません。")
        return

    print("物体認識を開始します。終了するにはキーボードの 'q' を押してください。")

    while True:
        # カメラから1フレーム読み込み
        ret, frame = cap.read()
        if not ret:
            print("フレームの取得に失敗しました。")
            break

        # YOLOv8で物体認識を実行（stream=Trueで動画処理を効率化）
        results = model(frame, stream=True)

        # 認識結果を描画したフレームを取得
        for result in results:
            annotated_frame = result.plot()

        # 画面に描画結果を表示
        cv2.imshow("YOLOv8 USB Camera", annotated_frame)

        # 'q' キーが押されたらループを抜けて終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 後片付け（カメラの解放とウィンドウのクローズ）
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
