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
        fast = 3
        left_flag = 0
        right_flag = 0
        max_speed =50
        
        left_sum = context.get('left_sum')
        right_sum = context.get('right_sum')
        left_min = context.get('left_min')
        right_min = context.get('right_min')
        left_max = context.get('left_max')
        right_max = context.get('right_max')
        pwm = context.get('pwm')

        if left_max==-9999 or right_max==-9999 or left_min==9999 or right_min==9999:
            pwm=0 
            return

        # 왼쪽 플래그 계산
        if left_sum < (left_min + (left_max - left_min) * 0.35):
            left_flag = slow
        elif left_sum < (left_min + (left_max - left_min) * 0.65):
            left_flag = maintain
        else:
            left_flag = fast

        # 오른쪽 플래그 계산
        if right_sum < (right_min + (right_max - right_min) * 0.35):
            right_flag = slow
        elif right_sum < (right_min + (right_max - right_min) * 0.65):
            right_flag = maintain
        else:
            right_flag = fast
        
        # 메인 로직
        if (left_sum <= (left_min + (left_max - left_min) * 0.1)) and (right_sum<=right_min + (right_max - right_min) * 0.1):
            pwm=0
        
        if left_flag+right_flag==0:
            pwm = pwm*0.8
                
        elif left_flag+right_flag>=3:
            if pwm==0:
                pwm=25
            else:
                if pwm>=max_speed:
                    pwm=max_speed
                else:
                    pwm = pwm*1.1
        
        context["pwm"] = pwm
        print("left flag : ", left_flag)
        print("right_flag : ", right_flag)
        print("sum : ",left_flag+right_flag)
        print((left_sum-left_min)/(left_max - left_min)*100)
        print((right_sum-right_min)/(right_max - right_min)*100)
        
    # # pitch 기반으로 오르막/내리막 감지
    # def calculate_slope(self, context):
    #     pitch = context.get("pitch")
    #     slope_status = "flat"

    #     if pitch > 5:
    #         slope_status = "uphill"
    #     elif pitch < -5:
    #         slope_status = "downhill"

    #     context["slope_status"] = slope_status
    #     print(f"[Slope 판단] Pitch: {pitch:.2f}°, 경사 상태: {slope_status}")

    # # 오르막/내리막에 따른 PWM 보정
    # def adjust_pwm_by_slope(self, context):
    #     pwm = context.get("pwm")
    #     slope_status = context.get("slope_status", "flat")

    #     if slope_status == "uphill":
    #         pwm *= 0.9  # 오르막이면 속도 살짝 줄이기
    #     elif slope_status == "downhill":
    #         pwm *= 0.85  # 내리막이면 더 많이 줄이기
    #     else:
    #         pass

    #     context["pwm"] = pwm
    #     print(f"[Slope 보정] 최종 PWM: {pwm:.2f}")


# # 속도 유지 없을 경우 로직
# class SpeedController:
#     def __init__(self):
#         pass

#     # 평균값 계산용
#     def calculate_row_sum(self, matrix):
#         if not matrix or len(matrix) != 16 or any(len(row) != 32 for row in matrix):
#             raise ValueError("입력 매트릭스는 16x32 형태여야 합니다.")

#         row_sum = []
#         for row in enumerate(matrix):
#             row_sum.append(sum(row))

#         return row_sum
    
#     # 왼쪽, 오른쪽 합 계산용
#     def calculate_sum(self, context):
#         fsr_matrix = context.get("fsr_matrix")
#         if not fsr_matrix or len(fsr_matrix) != 16:
#             raise ValueError("context에 유효한 fsr_matrix가 없습니다.")

#         left_sum = 0
#         right_sum = 0

#         for row in fsr_matrix:
#             left_sum += sum(row[0:16])  
#             right_sum += sum(row[16:32]) 

#         context["left_sum"] = left_sum
#         context["right_sum"] = right_sum

#     # 속도 제어
#     def calculate_pwm(self, context):   
#         stop = 0
#         slow = 1
#         fast = 3
#         left_flag = 0
#         right_flag = 0
#         max_speed =50
        
#         left_sum = context.get('left_sum')
#         right_sum = context.get('right_sum')
#         left_min = context.get('left_min')
#         right_min = context.get('right_min')
#         left_max = context.get('left_max')
#         right_max = context.get('right_max')
#         pwm = context.get('pwm')

#         if left_max==-9999 or right_max==-9999 or left_min==9999 or right_min==9999:
#             pwm=0 
#             return

#         # 왼쪽 플래그 계산
#         if left_sum < (left_min + (left_max - left_min) * 0.3):
#             left_flag = stop
#         elif left_sum < (left_min + (left_max - left_min) * 0.6):
#             left_flag = slow
#         else:
#             left_flag = fast

#         # 오른쪽 플래그 계산
#         if right_sum < (right_min + (right_max - right_min) * 0.3):
#             right_flag = stop
#         elif right_sum < (right_min + (right_max - right_min) * 0.6):
#             right_flag = slow
#         else:
#             right_flag = fast
        
#         # 메인 로직
#         if left_flag+right_flag==stop+stop:
#             pwm=0
#         elif left_flag+right_flag==stop+slow:
#             pwm=pwm*0.9
#         elif left_flag+right_flag>=stop+fast:
#             if pwm==0:
#                 pwm=25
#             else:
#                 if pwm>=max_speed:
#                     pwm=max_speed
#                 else:
#                     pwm = pwm*1.1
        
#         context["pwm"] = pwm
#         print("left flag : ", left_flag)
#         print("right_flag : ", right_flag)
#         print("sum : ",left_flag+right_flag)
#         print((left_sum-left_min)/(left_max - left_min)*100)
#         print((right_sum-right_min)/(right_max - right_min)*100)