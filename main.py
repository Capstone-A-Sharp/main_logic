from serial_handler import connect_arduino, send_pwm_to_arduino
from control_logic import SpeedController
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line
from calibration import Calibration

# 시리얼 포트 초기화
ser = connect_arduino()

controller = SpeedController()
calibration = Calibration()

# 센서 상태 정보 저장용 context
context = {
    # 기울기
    "pitch": 0.0,
    
    # 전체 16x32 fsr_matrix
    "fsr_matrix": [[0] * 32 for _ in range(16)],
    
    # 좌우 합산 압력
    "left_sum": 0,
    "right_sum": 0,
    "left_min": 9999,
    "right_min": 9999,
    "left_max": -9999,
    "right_max": -9999,
    "pwm": 0,
    
    # 캘리브레이션 스위치
    "calib_switch": 0
}

def update_wrapper(*args):
    fig, ax, cax = start_visualization(context)

    buffer = ""

    while True:
        # 시리얼 데이터 읽기
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                continue

            if line == "END":
                if buffer:
                    try:
                        # 시리얼 통신으로 값 받아오기
                        parse_serial_line(buffer, context)
                        
                        # 실시간 압력센서값 그래프로 나타내기
                        update_image(fig, ax, cax, context)

                        # 디버깅
                        print(f"Pitch 값: {context.get('pitch')}")
                        print("FSR 매트릭스 값:")
                        for idx, row in enumerate(context.get('fsr_matrix', [])):
                            print(f"Row {idx}: {row}")

                        # 압력센서 left, right 합 계산
                        controller.calculate_sum(context)
                        print(f"Left 합: {context.get('left_sum')}, Right 합: {context.get('right_sum')}")

                        # calib_switch ON일 경우 : 캘리브레이션 진행
                        if context.get('calib_switch')==1 :
                            print("calibration 시작")
                            calibration.calculate_minmax(context)
                            print(f"Left Min: {context.get('left_min')}, Left Max 합: {context.get('left_max')}")
                            print(f"Right Min: {context.get('right_min')}, Right Max 합: {context.get('right_max')}")
                            
                        # 메인 로직 진행
                        else :
                            controller.calculate_pwm(context)
                            print(f"PWM 값: {context.get('pwm')}")
                            
                        # 오르막, 내리막 계산
                        #controller.calculate_slope(context)

                        # 오르막, 내리막일 경우 pwm 갱신
                        #controller.adjust_pwm_by_slope(context)

                        # 시리얼로 pwm 값 최종 전송
                        send_pwm_to_arduino(ser, context)
                        
                    except Exception as e:
                        print("[Error] JSON 파싱 중 문제 발생:", e)
                    finally:
                        buffer = ""
            else:
                buffer += line

if __name__ == "__main__":
    update_wrapper()