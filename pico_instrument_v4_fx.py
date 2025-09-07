# pico_instrument_v4_fx.py
import machine
import time
import math # ★★★ ビブラート計算のためにmathをインポート ★★★

# --- ピンと音階の設定 (変更なし) ---
button_pins = [
    machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
]
notes = [262, 294, 330, 349]
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(buzzer_pin)
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# --- メインループ変数 ---
print("Pico Instrument v4.0 FX Enabled!")
current_playing_button = -1
current_note_freq = 0
pitch_bend_effect = 0
vibrato_effect_active = False # ★★★ ビブラート効果用の旗を追加 ★★★
vibrato_counter = 0 # ★★★ ビブラートの波を作るためのカウンター ★★★

# --- メインループ ---
while True:
    # --- Micro:bitからのコマンド受信処理 ---
    if uart.any():
        command = uart.read().strip()
        if command == b'LEFT':
            pitch_bend_effect = -1
        elif command == b'RIGHT':
            pitch_bend_effect = 1
        elif command == b'CENTER':
            pitch_bend_effect = 0
        # ★★★ 新しいコマンドの処理を追加 ★★★
        elif command == b'FX_ON':
            vibrato_effect_active = True
        elif command == b'FX_OFF':
            vibrato_effect_active = False

    # --- ボタン入力処理 (変更なし) ---
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
    # もし、何かのボタンが押されているなら...
    if current_playing_button != -1:
        # 1. ピッチベンド処理
        if pitch_bend_effect != 0:
            current_note_freq += pitch_bend_effect
        
        # 2. ★★★ ビブラート処理 ★★★
        if vibrato_effect_active:
            # sin波を使って滑らかな揺れを作る
            vibrato_amount = int(math.sin(vibrato_counter * 0.5) * 5)
            buzzer.freq(current_note_freq + vibrato_amount)
            vibrato_counter += 1
        else:
            # エフェクトがOFFなら、元の音程に戻す
            buzzer.freq(current_note_freq)

    time.sleep_ms(10)