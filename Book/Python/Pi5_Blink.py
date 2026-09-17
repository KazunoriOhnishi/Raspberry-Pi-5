from gpiozero import LED
from time import sleep

led = LED(17)  # LEDのピン番号設定

while True:
    led.on()   # LED点灯
    sleep(0.5) # 待機時間0.5秒
    led.off()  # LED消灯
    sleep(0.5) # 待機時間0.5秒