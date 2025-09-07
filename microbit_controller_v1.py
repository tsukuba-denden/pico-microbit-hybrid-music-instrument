# microbit_controller_v1.py
from microbit import *

# シリアル通信の初期設定
# 通信速度をPicoと合わせます (115200)
# 送信(TX)にP0ピン、受信(RX)にP1ピンを指定します
uart.init(baudrate=115200, tx=pin0, rx=pin1)

# 準備完了のサインとして、LEDにハートマークを表示
display.show(Image.HEART)

# 無限ループでボタンが押されるのを待ちます
while True:
    # もし、Aボタンが「押された瞬間」だったら
    if button_a.was_pressed():
        # 押されたことが分かるように、矢印を表示
        display.show(Image.ARROW_W)
        
        # Picoに向けて、コマンド 'A' を送信！
        uart.write('A')
        
        # 0.2秒待ってから、元のハートマークに戻す
        sleep(200)
        display.show(Image.HEART)