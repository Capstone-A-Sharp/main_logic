from serial_handler import connect_arduino
from control_logic import SpeedController
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line
from calibration import Calibration
import time

# 시리얼 포트 초기화
ser = connect_arduino()

controller = SpeedController()
calibration = Calibration()

# 센서 상태 정보 저장용 context
context = {
    "pitch": 0.0,
    "fsr_matrix_left": [[0] * 16 for _ in range(16)],  
    "fsr_matrix_right": [[0] * 16 for _ in range(16)],  
    "left_sum": 0,
    "right_sum": 0,
    "calib_switch": 0, 
    "left_min" : 0,
    "right_min" : 0,
    "left_max" : 999,
    "right_max" : 999
}

def update_wrapper(*args):

    fig, ax, cax = start_visualization(context)

    buffer = ""

    while True:
        # now = time.time()

        # 시리얼 데이터 읽기
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                continue

            if line == "END":
                if buffer:
                    try:
                        result = parse_serial_line(buffer, context)
                        update_image(fig, ax, cax, context)

                        if result:
                            # 디버깅
                            print("[Sensor 1 결과] ----------------")
                            print(f"Pitch 값: {context.get('pitch')}")

                            print("FSR 매트릭스 값:")
                            for idx, row in enumerate(context.get('fsr_matrix', [])):
                                print(f"Row {idx}: {row}")

                            controller.calculate_sum(context)
                            print(f"[PWM 계산] Left 합: {context.get('left_sum')}, Right 합: {context.get('right_sum')}")

                            # calib_switch ON일 경우 : 캘리브레이션 진행
                            if context.get('calib_switch')==1 :
                                calibration.calculate_minmax(context)
                            # 메인 로직 진행
                            else :
                                controller.calculate_pwm(context)

                    except Exception as e:
                        print("[Error] JSON 파싱 중 문제 발생:", e)
                    finally:
                        buffer = ""
            else:
                buffer += line


# 진입점
if __name__ == "__main__":
    update_wrapper()
