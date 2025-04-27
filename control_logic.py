# control_logic.py

class SpeedController:
    def __init__(self):
        pass

    # 평균값 계산용
    def calculate_row_sum(self, matrix):
        if not matrix or len(matrix) != 16 or any(len(row) != 32 for row in matrix):
            raise ValueError("입력 매트릭스는 16x32 형태여야 합니다.")

        row_sum = []
        for idx, row in enumerate(matrix):
            row_sum.append(sum(row))

        return row_sum
    
    # 속도 제어 용
    def caculate_pwm(self,context):
        
        pass
        
