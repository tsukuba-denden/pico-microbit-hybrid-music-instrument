# pico_instrument_v5.1_bugfix.py
import machine
import time
import math

# --- ピンと音階の設定 (変更なし) ---
button_pins = [
    machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP), 
    machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP), 
    machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP), 
    machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
]
notes = [262, 294, 330, 349, 392, 440, 494, 523, 587]

# --- 以下の設定も変更なし ---
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(buzzer_pin)
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
print("Pico Instrument v5.1 Bugfixed! Ready!")
current_playing_button = -1
current_note_freq = 0
pitch_bend_effect = 0
vibrato_effect_active = False
vibrato_counter = 0

# --- メインループ ---
while True:
    # (コマンド受信処理、ボタン入力処理は変更なし)
    if uart.any():
        command = uart.read().strip()
        if command == b'LEFT': pitch_bend_effect = -1
        elif command == b'RIGHT': pitch_bend_effect = 1
        elif command == b'CENTER': pitch_bend_effect = 0
        elif command == b'FX_ON': vibrato_effect_active = True
        elif command == b'FX_OFF': vibrato_effect_active = False

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
        
    # --- エフェクト処理 ---
    if current_playing_button != -1:
        # 1. ピッチベンド処理
        if pitch_bend_effect != 0:
            current_note_freq += pitch_bend_effect
        
        # 2. ビブラート処理
        final_freq = current_note_freq # まずは基本の周波数を設定
        if vibrato_effect_active:
            vibrato_amount = int(math.sin(vibrato_counter * 0.5) * 5)
            final_freq += vibrato_amount # ビブラート効果を追加
            vibrato_counter += 1

        # ★★★ ここに安全装置を追加！ ★★★
        # もし周波数が低くなりすぎたら、最低でも20Hzにする
        if final_freq < 20:
            final_freq = 20
        # もし周波数が高くなりすぎたら、最高でも20000Hzにする
        if final_freq > 20000:
            final_freq = 20000
            
        # 安全装置を通った、最終的な周波数で音を鳴らす
        buzzer.freq(final_freq)

    time.sleep_ms(10)