import numpy as np


# 사용자 기준으로 압력 측정 로직
class Calibrator:
    def __init__(self):
        self.min_pressure = None
        self.max_pressure = None

    def record_min_pressure(self, avg_values):
        self.min_pressure = np.mean(avg_values)

    def record_max_pressure(self, avg_values):
        self.max_pressure = np.mean(avg_values)

    def get_threshold(self):
        if self.min_pressure is not None and self.max_pressure is not None:
            return self.max_pressure - self.min_pressure
        return None
