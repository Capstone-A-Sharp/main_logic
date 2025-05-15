from typing import Tuple

class SpeedController:
    def __init__(self) -> None:
        self.pitch_history = []
        self.SPEED = {'slow': 0, 'maintain': 1, 'fast': 3}
        self.PITCH_STATE = {'flat': 0, 'uphill': 1, 'downhill': -1}
        self.MAX_SPEED = 40
        self.MIN_PWM = 18

    # ✨ Outlier Filter 적용 (개선된 버전)
    def filter_pitch(self, new_pitch: float, threshold: float = 3.0, window_size: int = 5) -> float:
        # 초기 데이터가 부족한 경우 무조건 입력값 사용
        if len(self.pitch_history) < window_size:
            self.pitch_history.append(new_pitch)
            return new_pitch

        # 윈도우 평균 계산
        window = self.pitch_history[-window_size:]
        avg_pitch = sum(window) / window_size

        # 이상치 여부 판단
        if abs(new_pitch - avg_pitch) > threshold:
            filtered_pitch = avg_pitch  # 이상치 감지 → 평균값으로 대체
        else:
            filtered_pitch = new_pitch  # 정상값 → 그대로 사용

        self.pitch_history.append(filtered_pitch)  # 필터링된 값으로 이력 갱신
        return filtered_pitch
    
    # 오르막/내리막 판별
    def get_slope_status(self, pitch: float) -> Tuple[str, int]:
        filtered_pitch = self.filter_pitch(pitch)
        if filtered_pitch > 5:
            slope_status = "uphill"
            pitch_flag = self.PITCH_STATE['uphill']
        elif filtered_pitch < -3:
            slope_status = "downhill"
            pitch_flag = self.PITCH_STATE['downhill']
        else:
            slope_status = "flat"
            pitch_flag = self.PITCH_STATE['flat']
        return slope_status, pitch_flag

    # 속도값 flag 판단
    def get_speed_flag(self, value: float, value_min: float, value_max: float) -> int:
        value_range = value_max - value_min
        ratio = (value - value_min) / value_range
        if ratio < 0.30:
            return self.SPEED['slow'], ratio
        elif ratio < 0.65:
            return self.SPEED['maintain'], ratio
        else:
            return self.SPEED['fast'], ratio

    # pwm 계산 (메인 로직)
    def calculate_pwm(self, context: dict) -> None:
        # 입력 값
        left_sum = context.get('left_sum')
        right_sum = context.get('right_sum')
        left_min = context.get('left_min')
        right_min = context.get('right_min')
        left_max = context.get('left_max')
        right_max = context.get('right_max')
        pwm = context.get('pwm')
        pitch = context.get("pitch")

        # 예외 처리
        if -9999 in (left_max, right_max) or 9999 in (left_min, right_min):
            context["pwm"] = 0
            return

        # ✨ Pitch 값에 따른 오르막/내리막 판별
        slope_status, pitch_flag = self.get_slope_status(pitch)

        # 왼쪽 속도 플래그
        left_flag, left_ratio = self.get_speed_flag(left_sum, left_min, left_max)

        # 오른쪽 속도 플래그
        right_flag, right_ratio = self.get_speed_flag(right_sum, right_min, right_max)

        total_flag = left_flag + right_flag

        print(f"left_flag: {left_flag}, right_flag: {right_flag}, sum: {total_flag}")
        print(f"left ratio: {left_ratio*100:.1f}%, right ratio: {right_ratio*100:.1f}%")
        print(f"[Pitch Filter] Raw: {pitch:.2f}, Filtered: {self.pitch_history[-1]:.2f}")
        print(f"[Slope 판단] 경사 상태: {slope_status}, PWM: {pwm:.2f}")
        
        # 정지 조건
        if left_ratio < 0.1 and right_ratio < 0.1:
            context["pwm"] = 0
            return

        # 감속 로직
        if total_flag == 0:
            if pwm <= self.MIN_PWM:
                pwm = self.MIN_PWM
            
            # 평지
            # elif pitch_flag == self.PITCH_STATE['flat']: 
            pwm *= 0.9
                
            # 오르막
            # elif pitch_flag == self.PITCH_STATE['uphill']:
            #    pwm *= 0.95
                
            # 내리막
            # elif pitch_flag == self.PITCH_STATE['downhill']:
            #    pwm *= 0.80

        # 증속 로직
        elif total_flag >= 3:
            if pwm == 0:
                pwm = 20
                
            else:
                pwm = min(pwm*1.08, self.MAX_SPEED)
                # # 평지
                # if pitch_flag == self.PITCH_STATE['flat']:
                #     pwm = min(pwm*1.08, self.MAX_SPEED)
                    
                # # 오르막
                # elif pitch_flag == self.PITCH_STATE['uphill']:
                #     pwm = min(pwm*1.3, self.MAX_SPEED*2)
                    
                # # 내리막
                # elif pitch_flag == self.PITCH_STATE['downhill']:
                #     pwm = min(pwm*1.05, self.MAX_SPEED*0.8)

        # 후진일 경우 0.5배
        if context["motor_switch"]==1:
            pwm=pwm*0.5
        
        # 출력
        context["pwm"] = pwm
