import serial
from config import SERIAL_PORT_NANO, BAUD_RATE


def connect_arduino():
    print("[안내] 아두이노 나노와 연결 중...")
    ser = serial.Serial(SERIAL_PORT_NANO, BAUD_RATE)
    print("[완료] 아두이노 나노와 연결되었습니다.")
    return ser
