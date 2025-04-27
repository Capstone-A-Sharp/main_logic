import json

import json

def parse_serial_line(line, context):
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        print("[Error] JSON 디코딩 실패:", line)
        return None

    # MPU9250 데이터 파싱
    mpu_data = data.get("MPU9250", {})

    context["pitch"] = mpu_data.get("pitch", 0.0)

    # FSR 데이터 파싱
    fsr_data = data.get("FSR", {})
    matrix = []
    for row_idx in range(16):
        row_key = f"row{row_idx}"
        row_data = fsr_data.get(row_key, [0]*32)

        # rowN 전체를 context에 저장
        context[f"fsr_row{row_idx}"] = row_data

        matrix.append(row_data)

    context["fsr_matrix"] = matrix  # 16x32 매트릭스도 같이 저장

    return {
        "mpu": mpu_data,
        "fsr": fsr_data
    }
