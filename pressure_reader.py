import numpy as np
from config import NUM_ROWS, NUM_COLS


# 압력 센서 데이터 하이패스필터 적용
def apply_hpf(data, threshold=20):
    return np.where(data > threshold, data, 0)


# 압력 센서 데이터 평균필터 적용
def apply_avg_filter(filtered_matrix):
    return np.mean(filtered_matrix, axis=1)


# 압력 센서 데이터 읽어오기
def process_pressure_sensor(matrix):
    filtered = apply_hpf(matrix)
    amplified = np.square(filtered) / 30
    avg_values = apply_avg_filter(amplified)
    print(f"[압력 처리] 평균 압력값: {avg_values}")
    return amplified, avg_values
