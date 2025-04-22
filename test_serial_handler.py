from unittest.mock import MagicMock
import types

# 반복 가능한 시리얼 데이터 생성 함수
def create_test_sequence():
    return iter([
        "PRESSURE1",
        *["10,20,30,40,50,60,70,80,90,70,60,50,40,30,20,16"] * 16,
        "END",
        "GYRO:UP",
        "SWITCH_CALIB:1",
        "SWITCH_DIR:1"
    ])

# 시리얼 모킹 객체 생성 함수
def get_mock_serial():
    mock = MagicMock()
    mock.in_waiting = True
    mock.read_data = create_test_sequence()
    mock.readline.side_effect = lambda: next(mock.read_data).encode()
    mock.is_open = True
    mock.write = lambda x: print(f"[모킹된 전송] {x.decode().strip()}")

    def reset_mock_read_data(self):
        self.read_data = create_test_sequence()
        self.readline.side_effect = lambda: next(self.read_data).encode()

    mock.reset_mock_read_data = types.MethodType(reset_mock_read_data, mock)
    return mock