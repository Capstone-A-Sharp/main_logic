import json

def parse_serial_line(line, context):
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        print("[Error] JSON 디코딩 실패:", line)
        return None

    # 자이로 센서 기울기값
    mpu_data = data.get("MPU9250", {})
    context["pitch"] = mpu_data.get("pitch", 0.0)

    # FSR 데이터 파싱
    fsr_data = data.get("FSR", {})
    matrix = []
    for row_idx in range(16):
        row_key = f"row{row_idx}"
        row_data = fsr_data.get(row_key, [0]*32)
        matrix.append(row_data)

    context["fsr_matrix"] = matrix 
    
    # calib_switch 데이터 파싱
    context["calib_switch"] = data.get("calib_switch", 0)
    
    # 🆕 Wheel_Speed 데이터 파싱
    wheel_data = data.get("Wheel_Speed", {})
    context["speedL"] = wheel_data.get("L", 0)
    context["speedR"] = wheel_data.get("R", 0)
    #print(f"[수신] Wheel_Speed - L: {context['speedL']}, R: {context['speedR']}")
