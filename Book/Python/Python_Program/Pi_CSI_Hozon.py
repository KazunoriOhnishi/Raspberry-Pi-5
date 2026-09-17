# Pi_CSI_Hozon.py

# Raspberry Pi でカメラ映像を表示・保存するプログラム
# Picamera2 + OpenCV

from picamera2 import Picamera2
import cv2

def main():
    # カメラを初期化（640x480でプレビュー）
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
    cam.start()

    # デジタルズームを解除（センサー全体を使用）
    try:
        sw, sh = cam.camera_properties["PixelArraySize"]
        cam.set_controls({"ScalerCrop": (0, 0, int(sw), int(sh))})
    except Exception:
        cam.set_controls({"ScalerCrop": (0, 0, 2592, 1944)})

    while True:
        # カメラ画像を取得（RGB→BGRに変換）
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2BGR)

        # そのまま表示
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):   # sキーで保存
            cv2.imwrite("frame.jpg", frame)
            print("Saved: frame.jpg")
        elif key == ord('q'): # qキーで終了
            break

    # 終了処理
    cv2.destroyAllWindows()
    cam.stop()

if __name__ == "__main__":
    main()
