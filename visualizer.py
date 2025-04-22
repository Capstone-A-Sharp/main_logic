import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from config import NUM_ROWS, NUM_COLS

plt.style.use('dark_background')
fig, ax = plt.subplots()
img = ax.imshow(np.zeros((NUM_ROWS, NUM_COLS)), cmap='inferno', interpolation='bilinear', vmin=0, vmax=100)
plt.colorbar(img, ax=ax, label="Pressure Intensity")
plt.title("Sensor (16x16)")

def start_visualization(update_func):
    ani = animation.FuncAnimation(fig, update_func, interval=100, blit=False, save_count=100)
    plt.show()
    return ani


def update_image(amplified_matrix):
    img.set_data(amplified_matrix)
    return [img]
