# Pi_Edge.py

# Raspberry Pi カメラ映像で Canny エッジ検出
# Picamera2 + OpenCV

from picamera2 import Picamera2
import cv2

def nothing(x):
    pass

def main():
    # カメラ初期化（640x480）
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
    cam.start()

    # デジタルズーム解除（フル視野）
    try:
        sw, sh = cam.camera_properties["PixelArraySize"]
        cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
    except Exception:
        cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

    # Canny パラメータ設定用スライダー
    cv2.namedWindow("Controls")
    cv2.createTrackbar("Low",  "Controls", 50, 255, nothing)
    cv2.createTrackbar("High", "Controls", 150, 255, nothing)

    while True:
        # カメラ画像（RGB→BGR）
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ぼかし（ノイズ低減）
        blur = cv2.GaussianBlur(gray, (5, 5), 1.0)

        # Trackbar の値を取得
        low  = cv2.getTrackbarPos("Low",  "Controls")
        high = cv2.getTrackbarPos("High", "Controls")
        high = max(high, low + 1)  # High は Low より大きく

        # Canny エッジ検出
        edges = cv2.Canny(blur, low, high)

        # 表示
        cv2.imshow("Original", frame)
        cv2.imshow("Blurred", blur)
        cv2.imshow("Edges",   edges)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):   # 終了
            break

    cv2.destroyAllWindows()
    cam.stop()

if __name__ == "__main__":
    main()
