# visualizer.py

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# 💡 블러 강도, 컬러맵 최대값 설정
BLUR_SIGMA = 0.3
VMAX = 20

def start_visualization(context):
    """
    시각화 초기화 (그래프 창 띄우기)
    """
    plt.ion()
    fig, ax = plt.subplots()
    matrix = np.zeros((16, 32))

    # 💡 vmax 수정
    cax = ax.imshow(matrix, cmap='plasma', interpolation='bicubic', vmin=0, vmax=VMAX)

    # 배경 검정
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # 글자 흰색
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='both', colors='white')

    colorbar = fig.colorbar(cax, ax=ax, label='Pressure Intensity')
    colorbar.ax.yaxis.label.set_color('white')
    colorbar.ax.tick_params(colors='white')

    ax.set_title('Real-Time Pressure Sensor Visualization (16x32)')

    return fig, ax, cax


def update_image(fig, ax, cax, context):
    """
    context에서 fsr_matrix를 읽어와서 이미지 업데이트 (Gaussian blur 조정)
    """
    matrix = context.get('fsr_matrix')

    if matrix is not None:
        matrix = np.array(matrix)

        if matrix.shape == (16, 32):
            blurred_matrix = gaussian_filter(matrix, sigma=BLUR_SIGMA)
            cax.set_data(blurred_matrix)
            fig.canvas.draw()
            fig.canvas.flush_events()
        else:
            print("[Warning] FSR 매트릭스 사이즈가 이상합니다:", matrix.shape)
    else:
        print("[Warning] FSR 매트릭스가 없습니다.")
