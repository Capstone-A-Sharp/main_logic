### main.py
from test_serial_handler import get_mock_serial  # 테스트용 시리얼
from control_logic import SpeedController
from calibration import Calibrator
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line  # 외부 파일로 분리된 파서 사용

# 시리얼 포트 대신 테스트용 시리얼 모듈 사용
ser = get_mock_serial()
controller = SpeedController()
calibrator = Calibrator()

# 센서 상태 정보 저장용 context
context = {
    "sensor": None,
    "reading": False,
    "row": 0,
    "matrix": None,
    "calib_mode": 0,
    "direction": 1,
    "slope_factor": 1.0,
}


# 보정 스위치가 활성화되었을 때 수행할 함수
def handle_calibration(avg_values):
    calibrator.record_max_pressure(avg_values)
    calibrator.record_min_pressure(avg_values)
    controller.update_threshold(calibrator.get_threshold())
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

    try:
        while ser.in_waiting:
            try:
                line = ser.readline()
                if isinstance(line, bytes):
                    line = line.decode().strip()
                else:
                    line = str(line).strip()

                result = parse_serial_line(line, context)
                if result:
                    amplified_matrix, avg_values = result
            except StopIteration:
                print("[테스트] 시리얼 데이터 재시작 (무한 반복)")
                if hasattr(ser, "reset_mock_read_data"):
                    ser.reset_mock_read_data()

    except Exception as e:
        print(f"[에러] 시리얼 읽기 중 오류 발생: {e}")

    if amplified_matrix is not None and avg_values is not None:
        if context["calib_mode"] == 1:
            handle_calibration(avg_values)
        else:
            return handle_control(avg_values, amplified_matrix)

    return []


# 프로그램 시작
if __name__ == "__main__":
    start_visualization(update_wrapper)
