# 시리얼 통신으로 들어오는 다양한 센서 데이터를 식별하고 분기 처리하는 모듈입니다.
import numpy as np
from pressure_reader import process_pressure_sensor


def parse_serial_line(line, context):
    if line.startswith("PRESSURE1") or line.startswith("PRESSURE2"):
        context["sensor"] = 1 if "1" in line else 2
        context["row"] = 0
        context["matrix"] = np.zeros((16, 16))
        context["reading"] = True

    elif line.startswith("SWITCH_CALIB"):
        context["calib_mode"] = int(line.split(":")[1])
        print(f"[보정 스위치] 상태: {context['calib_mode']}")

    elif line.startswith("GYRO"):
        direction = line.split(":")[1].strip()
        if direction == "UP":
            context["slope_factor"] = 1.2
        elif direction == "DOWN":
            context["slope_factor"] = 0.8
        else:
            context["slope_factor"] = 1.0
        print(f"[자이로] 경사 방향: {direction}, 속도 계수: {context['slope_factor']}")

    elif line.startswith("SWITCH_DIR"):
        context["direction"] = int(line.split(":")[1])
        print(f"[방향 스위치] 전진(1)/후진(0): {context['direction']}")

    elif line == "END" and context.get("reading"):
        context["reading"] = False
        return process_pressure_sensor(context["matrix"])

    elif context.get("reading"):
        values = line.split(",")
        if len(values) == 16:
            context["matrix"][context["row"]] = list(map(int, values))
            context["row"] += 1

    return None
