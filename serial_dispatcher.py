import json

def parse_serial_line(line, context):
    """
    시리얼로 수신한 JSON 문자열을 파싱하고 context를 업데이트한다.

    Args:
        line (str): 시리얼로 읽은 한 줄 문자열 (JSON 형식 기대)
        context (dict): 센서 상태를 저장하는 컨텍스트

    Returns:
        dict: 업데이트된 결과 데이터 (필요시)
    """
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        print("[Error] JSON 디코딩 실패:", line)
        return None

    # MPU9250 데이터 처리
    mpu_data = data.get("MPU9250")
    if mpu_data:
        context["sensor_1"] = mpu_data
        context["reading_1"] = True

    # FSR 데이터 처리
    fsr_data = data.get("FSR")
    if fsr_data:
        matrix = []
        for row_idx in range(16):
            row_key = f"row{row_idx}"
            if row_key in fsr_data:
                matrix.append(fsr_data[row_key])
            else:
                print(f"[Warning] FSR 데이터에 {row_key} 없음")
                matrix.append([0] * 32)  # 비어있으면 0으로 채운 32칸 row

        context["sensor_2"] = fsr_data
        context["matrix_2"] = matrix
        context["reading_2"] = True
        context["row_2"] = len(matrix)

    return {
        "mpu": mpu_data,
        "fsr": fsr_data
    }
