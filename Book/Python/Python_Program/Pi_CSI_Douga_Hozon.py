# Pi_CSI_Douga_Hozon.py
from picamera2 import Picamera2
picam2 = Picamera2()
# 解像度を1920x1080に設定
video_config = picam2.create_video_configuration(
    main={"size": (1920, 1080)} 
)
# 設定の適用
picam2.configure(video_config)
# 動画撮影の開始と5秒後の自動停止
picam2.start_and_record_video("test_Hozon.mp4", duration=5)
# カメラの停止
picam2.stop()
