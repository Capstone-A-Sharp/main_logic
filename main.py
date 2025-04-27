from serial_handler import connect_arduino
from control_logic import SpeedController
from visualizer import start_visualization, update_image
from serial_dispatcher import parse_serial_line
import time

# 시리얼 포트 초기화
ser = connect_arduino()

controller = SpeedController()

# 센서 상태 정보 저장용 context
context = {
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

                            # 메인 로직 
                            if(context.get('switch')==1){ # 캘리브레이션 진행
                                controller.
                            }else{ # 메인 로직 진행
                                
                            }
                            
                            fsr_matrix = context.get('fsr_matrix')
                            row_sum = controller.calculate_row_sum(fsr_matrix)

                            # 디버깅
                            print("[Row 별 평균 압력]")
                            for idx, sum in enumerate(row_sum):
                                print(f"Row {idx} 압력합: {sum:.2f}")

                    except Exception as e:
                        print("[Error] JSON 파싱 중 문제 발생:", e)
                    finally:
                        buffer = ""
            else:
                buffer += line


# 진입점
if __name__ == "__main__":
    update_wrapper()
