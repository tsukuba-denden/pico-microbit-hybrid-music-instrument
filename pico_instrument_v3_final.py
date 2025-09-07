# pico_instrument_v3_final.py
import machine
import time

# --- ピンと音階の設定 ---
button_pins = [
    machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
]
notes = [262, 294, 330, 349]
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(buzzer_pin)

# --- ★★★ Micro:bitとの通信設定を追加 ★★★ ---
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# --- メインループ変数 ---
print("Pico Instrument v3.0 Final! Pitch Bend Enabled!")
current_playing_button = -1
current_note_freq = 0
pitch_bend_effect = 0 # 0:変化なし, -1:下げる, 1:上げる

# --- メインループ ---
while True:
    # --- ★★★ Micro:bitからのコマンド受信処理 ★★★ ---
    if uart.any():
        command = uart.read().strip()
        if command == b'LEFT':
            pitch_bend_effect = -1 # 音を下げるモードに
        elif command == b'RIGHT':
            pitch_bend_effect = 1  # 音を上げるモードに
        elif command == b'CENTER':
            pitch_bend_effect = 0  # 変化を止めるモードに

    # --- ボタン入力処理 ---
    pressed_button = -1
    for i in range(len(button_pins)):
        if button_pins[i].value() == 0:
            pressed_button = i
            break

    if pressed_button != current_playing_button:
        if pressed_button != -1:
            current_note_freq = notes[pressed_button]
            buzzer.freq(current_note_freq)
            buzzer.duty_u16(32768)
        else:
            buzzer.duty_u16(0)
        current_playing_button = pressed_button
        
    # --- ★★★ ピッチベンド処理 ★★★ ---
    # もし、何かのボタンが押されていて、かつピッチベンド効果がONなら
    if current_playing_button != -1 and pitch_bend_effect != 0:
        # 現在の周波数を少しずつ変化させる
        current_note_freq += pitch_bend_effect
        buzzer.freq(current_note_freq)

    time.sleep_ms(10)