class SpeedController:
    def __init__(self):
        pass

    # 평균값 계산용
    def calculate_row_sum(self, matrix):
        if not matrix or len(matrix) != 16 or any(len(row) != 32 for row in matrix):
            raise ValueError("입력 매트릭스는 16x32 형태여야 합니다.")

        row_sum = []
        for row in enumerate(matrix):
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
            
        slow = 0
        maintain = 1
        fast = 4
        left_flag = 0
        right_flag = 0
        
        left_sum = context.get('left_sum')
        right_sum = context.get('right_sum')
        left_min = context.get('left_min')
        right_min = context.get('right_min')
        left_max = context.get('left_max')
        right_max = context.get('right_max')
        pwm = context.get('pwm')
    

        # 왼쪽 플래그 계산
        if left_sum < (left_min + (left_max - left_min) * 0.3):
            left_flag = slow
        elif left_sum < (left_min + (left_max - left_min) * 0.6):
            left_flag = maintain
        else:
            left_flag = fast

        # 오른쪽 플래그 계산
        if right_sum < (right_min + (right_max - right_min) * 0.3):
            right_flag = slow
        elif right_sum < (right_min + (right_max - right_min) * 0.6):
            right_flag = maintain
        else:
            right_flag = fast
            
        if (left_sum >=left_min and left_sum < left_min*1.1) and (right_sum >=right_min and right_sum < right_min*1.1):
            pwm=0
        
        if left_flag+right_flag==0 or left_flag+right_flag==1:
            pwm = pwm*0.9
        elif left_flag+right_flag==2:
            pwm = pwm
        elif left_flag+right_flag>3:
            pwm = pwm*1.1
        
        context["pwm"] = pwm