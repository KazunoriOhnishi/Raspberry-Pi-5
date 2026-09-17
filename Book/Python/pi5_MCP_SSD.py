# pi5_MPU_SSD.py

import time
import board
import busio
import math
import adafruit_ssd1306
import adafruit_mpu6050
from PIL import Image, ImageDraw

# 1. I2Cを開始
i2c = busio.I2C(board.SCL, board.SDA)
# 2. SSD1306 OLEDの初期化 (アドレス 0x3C)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
# 3. MPU6050の初期化 (改行して分けました)
mpu = adafruit_mpu6050.MPU6050(i2c)

# 4. 表示用画像の準備
image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)

#float angle
#float Gyro_x

while True:   
    # 加速度の取得
    ax, ay, az = mpu.acceleration

    Angle = -math.atan2(ay,az) *(180/3.14159)

    # ジャイロの取得
    gx, gy, gz = mpu.gyro

    Gyro_x = -gx/1.31

    # 温度の取得
    temperature = mpu.temperature
    
    # 画面を消去 (真っ黒にする)
    draw.rectangle((0, 0, 127, 63), outline=0, fill=0)
    
    # OLEDに表示する文字を描画
    draw.text((0, 0),  "MPU6050", fill=255)

    draw.text((0, 15), "Angle:{:5.1f}".format(Angle), fill=255)
    draw.text((0, 30), "Gyro_x:{:5.1f}".format(Gyro_x), fill=255)
    
#    draw.text((0, 32), "A X:{:5.1f}".format(ax), fill=255)    
    draw.text((0, 45), "Temp:{:5.1f} C".format(temperature), fill=255)    
#    draw.text((70, 44), "G:{:4.1f}".format(gx), fill=255)
    
    # OLEDへ転送して表示 (改行して分けました)
    display.image(image)
    display.show()
    
    time.sleep(0.5)
