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
        max_speed = 40
        pitch_upcount=0 #오르막 상태를 얼마나 유지하는지 셈
        pitch_downcount=0 # 내리막 상태를 얼마나 유지하는지 셈
        
        left_sum = context.get('left_sum')
        right_sum = context.get('right_sum')
        left_min = context.get('left_min')
        right_min = context.get('right_min')
        left_max = context.get('left_max')
        right_max = context.get('right_max')
        pwm = context.get('pwm')
        
        pitch = context.get("pitch")
        pitch_flag=0
        flat = 0
        uphill=1
        downhill=-1
        slope_status = "flat"

        if pitch > 15: ################################################### 테스트 후 수정하기
            slope_status = "uphill"
            pitch_upcount+=1
        elif pitch < -15: ################################################ 테스트 후 수정하기
            slope_status = "downhill"
            pitch_downcount+=1
        else:
            slope_status = "flat"
            pitch_upcount=0 
            pitch_downcount=0


        if slope_status == "uphill":
            pitch_flag=uphill
        elif slope_status == "downhill":
            pitch_flag=downhill  # 내리막이면 더 많이 줄이기
        else:
            pitch_flag=flat


        if left_max==-9999 or right_max==-9999 or left_min==9999 or right_min==9999:
            context["pwm"] = 0
            return

        # 왼쪽 플래그 계산
        if left_sum < (left_min + (left_max - left_min) * 0.30):
            left_flag = slow
        elif left_sum < (left_min + (left_max - left_min) * 0.65):
            left_flag = maintain
        else:
            left_flag = fast

        # 오른쪽 플래그 계산
        if right_sum < (right_min + (right_max - right_min) * 0.30):
            right_flag = slow
        elif right_sum < (right_min + (right_max - right_min) * 0.65):
            right_flag = maintain
        else:
            right_flag = fast
        
        # 메인 로직
        if (left_sum <= (left_min + (left_max - left_min) * 0.1)) and (right_sum<=right_min + (right_max - right_min) * 0.1):
            context["pwm"] = 0
            return 
        
        # 감속 부분
        if left_flag+right_flag==0:
            if pwm<=18:
                pwm=18 # 최저 속도를 18cm/s로 설정
            elif pitch_flag==flat:
                pwm = pwm*0.9
                
            elif pitch_flag==uphill:
                if pitch_upcount>15:
                    pwm = pwm*0.92  ############################################################################ 오르막에서는 감속이 느리게 0.92부분 테스트 후 수정
                else:
                    pwm = pwm*0.9  ##################################################### downcount 15보다 작을때까진 평지로 인식
                    
            elif pitch_flag==downhill:
                if pitch_downcount>15:
                    pwm = pwm*0.85 ########################################################################## 내리막에서는 감속이 빠르게 0.85부분 테스트 후 수정
                else:
                    pwm = pwm*0.9  ##################################################### downcount 15보다 작을때까진 평지로 인식
 
        # 증속 부분 
        elif left_flag+right_flag>=3:
            if pwm==0:
                pwm=20
            else:
                if pitch_flag==flat:
                    if pwm>=max_speed:
                        pwm=max_speed
                    else:
                        pwm = pwm*1.1
                        
                elif pitch_flag==uphill:
                    if pitch_upcount>15: ##################  15 기준 수정
                        if pwm>=max_speed*1.1:
                            pwm=max_speed*1.1 ########################### uphill에서는 최고 속도 제한이 10퍼 증가
                        else:
                            pwm = pwm*1.12 ################################## uphill에서는 평지보다 증속이 빠름 1.12 부분 테스트 후 수정
                    else:
                        pwm = pwm*1.1      #################################### upcount 15보다 작으면 평지 취급
                        
                elif pitch_flag==downhill:
                    if pitch_downcount>15: ######################### 15 기준 수정
                        if pwm>=max_speed*0.85:
                            pwm=max_speed*0.85 ################################ downhill에서는 평지보다 최고 속도 제한이 15퍼 감소
                        else:
                            pwm = pwm*1.06 ##################################### downhill에서는 평지보다 증속이 느림 1.06 부분 테스트 후 수정
                    else:
                        pwm = pwm*1.1   ######################################### downcount 15보다 작으면 평지 취급
                    

        context["pwm"] = pwm
        print("left flag : ", left_flag)
        print("right_flag : ", right_flag)
        print("sum : ",left_flag+right_flag)
        print((left_sum-left_min)/(left_max - left_min)*100)
        print((right_sum-right_min)/(right_max - right_min)*100)
        
        print(f"[Slope 판단] Pitch: {pitch:.2f}°, 경사 상태: {slope_status}")
        print(f"[Slope 보정] 최종 PWM: {pwm:.2f}")


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