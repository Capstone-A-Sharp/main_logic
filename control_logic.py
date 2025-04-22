from config import BASE_PWM

class SpeedController:
    def __init__(self, max_speed=35, alpha=0.8):
        self.speed = BASE_PWM
        self.max_speed = max_speed
        self.alpha = alpha
        self.threshold = None  # 기준 압력값

    def update_threshold(self, threshold):
        self.threshold = threshold
        print(f"[보정] 기준 압력값 설정됨: {threshold:.2f}")

    def compute_speed(self, avg_values, ser, slope_factor, direction):
        if self.threshold is None:
            print("[경고] 기준 압력이 설정되지 않았습니다. 속도 계산 생략.")
            return self.speed

        push_sum = sum(avg_values[7:])  # 손바닥 영역의 압력 합
        ratio = push_sum / self.threshold

        # 속도 제어 로직
        if ratio >= 0.6:
            self.speed = min(self.speed * 1.1, self.max_speed)
            print("[속도 증가] 강하게 쥠 감지됨.")
        elif ratio < 0.3:
            self.speed = max(self.speed * 0.9, 0)
            print("[속도 감소] 힘이 거의 없음.")
        else:
            print("[속도 유지] 적당한 힘 유지 중.")

        # 경사 보정 적용
        adjusted_speed = self.speed * slope_factor
        adjusted_speed = min(adjusted_speed, self.max_speed)

        # 방향 보정 (후진일 경우 음수)
        pwm_signal = int(adjusted_speed) if direction == 1 else -int(adjusted_speed)

        # 시리얼로 PWM 값 전송
        if ser.is_open:
            ser.write(f"{pwm_signal}\n".encode())
            print(f"[PWM 전송] 값: {pwm_signal} (기본: {self.speed:.2f}, 경사 계수: {slope_factor}, 방향: {'전진' if direction==1 else '후진'})")

        return self.speed
