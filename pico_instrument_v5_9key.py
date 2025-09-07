# pico_instrument_v5_9key.py
import machine
import time
import math

# --- ピンと音階の設定 (9ボタン用に拡張！) ---

# ★★★ 接続したピンに合わせて、リストを9個に拡張 ★★★
button_pins = [
    machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン1 (一番右)
    machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン2
    machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン3
    machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン4
    machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン5
    machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP),  # ボタン6
    machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP),  # ボタン7
    machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP),  # ボタン8
    machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)   # ボタン9 (一番左)
]

# ★★★ 音階リストも9個に拡張 (ドレミファソラシドレ) ★★★
notes = [
    262,  # C4 (ド)
    294,  # D4 (レ)
    330,  # E4 (ミ)
    349,  # F4 (ファ)
    392,  # G4 (ソ)
    440,  # A4 (ラ)
    494,  # B4 (シ)
    523,  # C5 (高いド)
    587   # D5 (高いレ)
]

# --- 以下のコードは変更ありません ---

# ブザーと通信の設定
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(buzzer_pin)
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# メインループ変数
print("Pico Instrument v5.0! 9-key Keyboard Ready!")
current_playing_button = -1
current_note_freq = 0
pitch_bend_effect = 0
vibrato_effect_active = False
vibrato_counter = 0

# メインループ
while True:
    # Micro:bitからのコマンド受信処理
    if uart.any():
        command = uart.read().strip()
        if command == b'LEFT':
            pitch_bend_effect = -1
        elif command == b'RIGHT':
            pitch_bend_effect = 1
        elif command == b'CENTER':
            pitch_bend_effect = 0
        elif command == b'FX_ON':
            vibrato_effect_active = True
        elif command == b'FX_OFF':
            vibrato_effect_active = False

    # ボタン入力処理
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
        
    # エフェクト処理
    if current_playing_button != -1:
        # 1. ピッチベンド処理
        if pitch_bend_effect != 0:
            current_note_freq += pitch_bend_effect
        
        # 2. ビブラート処理
        if vibrato_effect_active:
            vibrato_amount = int(math.sin(vibrato_counter * 0.5) * 5)
            buzzer.freq(current_note_freq + vibrato_amount)
            vibrato_counter += 1
        else:
            buzzer.freq(current_note_freq)

    time.sleep_ms(10)