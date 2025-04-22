import numpy as np

# 사용자 기준으로 압력 측정 로직
class Calibrator:
    def __init__(self):
        self.min_pressure = float('inf')     # 보정 시작 후 들어온 최소 압력값
        self.max_pressure = float('-inf')    # 보정 시작 후 들어온 최대 압력값

    def update_pressure_extremes(self, avg_values):
        # 보정 도중 반복 호출되며, 평균 압력의 최소/최댓값을 계속 갱신
        current = np.mean(avg_values)
        if current < self.min_pressure:
            self.min_pressure = current
            print(f"[보정] 현재 최소 압력 갱신됨: {self.min_pressure:.2f}")
        if current > self.max_pressure:
            self.max_pressure = current
            print(f"[보정] 현재 최대 압력 갱신됨: {self.max_pressure:.2f}")

    def get_threshold(self):
        # 최대 압력 - 최소 압력 → 기준 압력값 반환
        if self.min_pressure < float('inf') and self.max_pressure > float('-inf'):
            threshold = self.max_pressure - self.min_pressure
            print(f"[보정 완료] 기준 압력값 계산됨: {threshold:.2f}")
            return threshold
        return None
