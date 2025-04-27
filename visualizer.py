import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 그래프 초기화
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((16, 32)), interpolation='nearest', vmin=0, vmax=1023)
plt.colorbar(im)

def update_image(result):
    """
    새로운 센서 데이터를 받아와서 이미지를 업데이트합니다.
    :param result: (matrix, sensor_id) 튜플 또는 None
    """
    if result is not None:
        matrix, sensor_id = result
        im.set_data(matrix)
    return im

def start_visualization(update_func):
    """
    matplotlib animation을 사용하여 주기적으로 update_func를 호출합니다.
    :param update_func: 주기적으로 호출할 함수
    """
    ani = animation.FuncAnimation(
        fig,
        update_func,
        interval=300,  # 업데이트 간격 (ms)
        blit=False
    )
    plt.show()
