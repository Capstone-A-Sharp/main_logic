from serial_handler import connect_arduino
# from control_logic import SpeedController
# from calibration import Calibrator
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line

# 시리얼 포트 초기화
ser = connect_arduino()

# controller = SpeedController()
# calibrator = Calibrator()

# 센서 상태 정보 저장용 context
context = {
    "sensor_1": None,
    "sensor_2": None,
    "reading_1": False,
    "reading_2": False,
    "row_1": 0,
    "row_2": 0,
    "matrix_1": None,
    "matrix_2": None,
    "calib_mode": 0,
    "direction": 1,
    "slope_factor": 1.0,
    "calib_done": False
}

amplified_sensors = {1: None, 2: None}

def update_wrapper(*args):
    global amplified_sensors

    buffer = ""  # JSON 덩어리 저장용 버퍼

    while True:
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                continue

            if line == "END":
                # END를 만나면 그제서야 파싱 시도
                if buffer:
                    try:
                        result = parse_serial_line(buffer, context)
                        if result:
                            print("[Sensor 1 결과] ----------------")
                            print(result)
                    except Exception as e:
                        print("[Error] JSON 파싱 중 문제 발생:", e)
                    finally:
                        buffer = ""  # 실패하든 성공하든 버퍼는 비워줘야 함
            else:
                # END를 만나기 전까지는 절대 파싱하지 말고 계속 이어붙이기만!
                buffer += line


# 진입점
if __name__ == "__main__":
    update_wrapper()
