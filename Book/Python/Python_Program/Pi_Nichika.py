# Pi_Nichika.py

# Raspberry Pi カメラ映像を3種類の二値化で表示・保存
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

    # デジタルズーム解除
    try:
        sw, sh = cam.camera_properties["PixelArraySize"]
        cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
    except Exception:
        cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

    # スライダーウィンドウ（手動しきい値用）
    cv2.namedWindow("Controls")
    cv2.createTrackbar("Manual TH", "Controls", 128, 255, nothing)

    while True:
        # カメラ画像（RGB→BGR）
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 手動しきい値
        th = cv2.getTrackbarPos("Manual TH", "Controls")
        _, bin_manual = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)

        # Otsu（二値化＋自動しきい値）
        _, bin_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 適応的二値化（局所的に判定）
        bin_adp = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )

        # 表示
        cv2.imshow("Original", frame)
        cv2.imshow("Manual",   bin_manual)
        cv2.imshow("Otsu",     bin_otsu)
        cv2.imshow("Adaptive", bin_adp)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # 保存
            cv2.imwrite("bin_manual.jpg",   bin_manual)
            cv2.imwrite("bin_otsu.jpg",     bin_otsu)
            cv2.imwrite("bin_adaptive.jpg", bin_adp)
            print("Saved.")
        elif key == ord('q'):   # 終了
            break

    cv2.destroyAllWindows()
    cam.stop()

if __name__ == "__main__":
    main()

