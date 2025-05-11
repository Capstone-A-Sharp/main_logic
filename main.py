from serial_handler import connect_arduino, send_pwm_to_arduino
from control_logic import SpeedController
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line
from calibration import Calibration

def init_context():
    return {
        "pitch": 0.0,
        "fsr_matrix": [[0] * 32 for _ in range(16)],
        "left_sum": 0,
        "right_sum": 0,
        "left_min": 9999,
        "right_min": 9999,
        "left_max": -9999,
        "right_max": -9999,
        "pwm": 0,
        "speedL": 0,
        "speedR": 0,
        "calib_flag": 0,
        "calib_switch": 0
    }

# ✨ Serial data로 Calibration 값 확인해서 로직 적용하기
def handle_serial_data(buffer, context, controller, calibration, ser):
    try:
        parse_serial_line(buffer, context)
        log_debug_info(context) # 로깅용

        if context["calib_switch"] == 1:
            if context["calib_flag"] == 0:
                calibration.reset_minmax(context)
                context["calib_flag"] = 1
                
            print("========== Calibration ==========")
            calibration.calculate_minmax(context)
        else:
            context["calib_flag"] = 0
            controller.calculate_pwm(context)
            print(f"PWM Value: {context['pwm']}")
            send_pwm_to_arduino(ser, context)

    except Exception as e:
        print("[Error] 데이터 처리 중 오류 발생:", e)

# ✨ 로깅용 함수
def log_debug_info(context):
    print(f"Pitch 값: {context['pitch']}")
    print(f"Left 합: {context['left_sum']}, Right 합: {context['right_sum']}")
    print(f"Left [Min: {context['left_min']}, Max: {context['left_max']}], "
          f"Right [Min: {context['right_min']}, Max: {context['right_max']}]")

# 메인 함수
def update_wrapper():
    ser = connect_arduino()
    controller = SpeedController()
    calibration = Calibration()
    context = init_context()

    # fig, ax, cax = start_visualization(context)
    buffer = ""

    while True:
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                continue

            if line == "END":
                if buffer:
                    handle_serial_data(buffer, context, controller, calibration, ser)
                    buffer = ""
            else:
                buffer += line

if __name__ == "__main__":
    update_wrapper()