# Pi_CSI_Capture.py

from picamera2 import Picamera2
picam2 = Picamera2()
# フル解像度で画像を取得するための設定
capture_config = picam2.create_still_configuration(
    # センサーのフル解像度を指定
    main={"size": picam2.camera_properties['PixelArraySize']}
)
# 設定の適用
picam2.configure(capture_config)

# カメラの開始
picam2.start()

# 画像のキャプチャ
picam2.capture_file("test_Hyouji.jpg")

# カメラの停止
picam2.stop()
