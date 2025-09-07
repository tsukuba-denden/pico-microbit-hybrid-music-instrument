# pico_instrument_v2.py
import machine
import time

# --- ピンと音階の設定 ---

# 4つのボタンをピン番号でリストにまとめる
button_pins = [
    machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン1
    machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン2
    machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP), # ボタン3
    machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)  # ボタン4
]

# 4つの音階（ドレミファ）を周波数でリストにまとめる
notes = [
    262,  # C4 (ド)
    294,  # D4 (レ)
    330,  # E4 (ミ)
    349   # F4 (ファ)
]

# ブザーをGP15に接続
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(buzzer_pin)


# --- メインループ ---
print("Pico Instrument v2.0 Ready. 4-key Piano!")

# 現在どのボタンが押されているかを記録する変数 (-1は何も押されていない状態)
current_playing_button = -1

while True:
    pressed_button = -1

    # 0番から3番までのボタンを順番にチェック
    for i in range(len(button_pins)):
        # ボタンが押されていたら (値が0なら)
        if button_pins[i].value() == 0:
            pressed_button = i
            break # 誰かが押されていたら、ループを抜ける

    # 状態に変化があったかチェック
    if pressed_button != current_playing_button:
        # もし新しいボタンが押されたなら
        if pressed_button != -1:
            note_to_play = notes[pressed_button]
            print("Playing note:", note_to_play)
            buzzer.freq(note_to_play)
            buzzer.duty_u16(32768)
        # もしボタンが離されたなら
        else:
            print("Sound stopped")
            buzzer.duty_u16(0)
        
        # 現在の状態を更新
        current_playing_button = pressed_button

    time.sleep_ms(10)