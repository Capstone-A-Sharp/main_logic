import serial
from config import SERIAL_PORT_NANO, BAUD_RATE

def connect_arduino():
    print("[안내] 아두이노 나노와 연결 중...")
    ser = serial.Serial(SERIAL_PORT_NANO, BAUD_RATE)
    print("[완료] 아두이노 나노와 연결되었습니다.")
    return ser

def send_pwm_to_arduino(ser, context):
    pwm_value = int(context.get("pwm"))  
    
    message = f"{pwm_value}\n"  # 문자열 + 개행문자
    try:
        ser.write(message.encode('utf-8'))  # UTF-8 인코딩 후 전송
        print(f"[시리얼 전송] PWM: {pwm_value}")
    except Exception as e:
        print("[Error] 시리얼 전송 실패:", e)
