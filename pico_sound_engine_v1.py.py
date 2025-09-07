# pico_instrument_v1.py
import machine
import time

# --- ピンの設定 ---

# 押しボタンをGP14に接続
# PULL_UP設定: ボタンが押されていない時は電圧が「高(High)」、押されると「低(Low)」になる
button_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# ブザーをGP15に接続
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
# 音を鳴らすためのPWMオブジェクトを作成
buzzer = machine.PWM(buzzer_pin)

# --- 定数の設定 ---
NOTE_C4 = 262  # ドの音の周波数 (Hz)

# --- メインループ ---
print("Pico Instrument v1.0 Ready. Press the button!")

# is_playingフラグ: 同じ音を何度も鳴らし始めないようにするための旗
is_playing = False

while True:
    # ボタンが押されたかチェック (PULL_UPなので、押されると値が0になる)
    if button_pin.value() == 0:
        # もし、まだ音が鳴っていないなら (is_playingがFalseなら)
        if not is_playing:
            print("Button Pressed: Playing C4")
            # ブザーの周波数を「ド」に設定
            buzzer.freq(NOTE_C4)
            # 音量50%で鳴らし始める
            buzzer.duty_u16(32768)
            # 「今、音が鳴っているよ」と旗を立てる
            is_playing = True
    # ボタンが離された場合
    else:
        # もし、さっきまで音が鳴っていたなら (is_playingがTrueなら)
        if is_playing:
            print("Button Released: Sound stopped")
            # 音を止める (音量を0にする)
            buzzer.duty_u16(0)
            # 「音は止まったよ」と旗を倒す
            is_playing = False

    # CPUに少しだけ休憩を与える（安定動作のため）
    time.sleep_ms(10)