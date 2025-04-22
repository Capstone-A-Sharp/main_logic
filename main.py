from serial_handler import connect_arduino
from control_logic import SpeedController
from calibration import Calibrator
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line

# 시리얼 포트 및 제어기 초기화
ser = connect_arduino()
controller = SpeedController()
calibrator = Calibrator()

# 센서 상태 정보 저장용 context
context = {
    "sensor": None,
    "reading": False,
    "row": 0,
    "matrix": None,
    "calib_mode": 0,          # 1: 보정 중, 0: 일반 제어 모드
    "direction": 1,
    "slope_factor": 1.0,
    "calib_done": False       # 보정 완료 여부
}

# 보정 스위치가 활성화되었을 때 (보정 중) 압력 추적 함수
def handle_calibration(avg_values):
    calibrator.update_pressure_extremes(avg_values)
    print("[보정] 압력 수집 중...")

# 보정 스위치가 꺼졌을 때 기준값 확정
def finalize_calibration():
    threshold = calibrator.get_threshold()
    if threshold is not None:
        controller.update_threshold(threshold)
        context["calib_done"] = True
        print("[보정] 기준 압력값 적용 완료.")
    context["calib_mode"] = 0

# 실질적인 속도 제어 수행 함수
def handle_control(avg_values, amplified_matrix):
    controller.compute_speed(
        avg_values, ser, context["slope_factor"], context["direction"]
    )
    return update_image(amplified_matrix)

# 센서 데이터 통합 처리 루프
def update_wrapper(*args):
    amplified_matrix, avg_values = None, None

    while ser.in_waiting:
        line = ser.readline().decode().strip()
        result = parse_serial_line(line, context)

        if result:
            amplified_matrix, avg_values = result

    if amplified_matrix is not None and avg_values is not None:
        if context["calib_mode"] == 1:
            handle_calibration(avg_values)
        elif not context["calib_done"]:
            finalize_calibration()
        else:
            return handle_control(avg_values, amplified_matrix)

    return []

# 프로그램 시작
if __name__ == "__main__":
    start_visualization(update_wrapper)
