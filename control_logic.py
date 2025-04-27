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
    
    # 왼쪽, 오른쪽 합 계산용
    def calculate_sum(self, context):
        fsr_matrix = context.get("fsr_matrix")
        if not fsr_matrix or len(fsr_matrix) != 16:
            raise ValueError("context에 유효한 fsr_matrix가 없습니다.")

        left_sum = 0
        right_sum = 0

        for row in fsr_matrix:
            left_sum += sum(row[0:16])  
            right_sum += sum(row[16:32]) 

        context["left_sum"] = left_sum
        context["right_sum"] = right_sum

    # 속도 제어
    def calculate_pwm(self, context):
        pass