import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import seaborn as sns
import sys

sns.set_style('darkgrid')
name = sys.argv[1]
coin = sys.argv[2]

def animate(i):
    data = pd.read_csv(f'./data/df_results_{name}.csv', sep=';').iloc[2:]
    data = data.iloc[2:]

    if i < len(data):
        data = data.iloc[:i]
    

    x = np.arange(len(data))
    y1 = data['y']
    y2 = data['y_pred']

    plt.cla()
    plt.rcParams["figure.figsize"] = (20,10)
    plt.xlabel('Minutes')
    plt.ylabel('Value')
    plt.plot(x, y1, label='True value', marker='o')
    plt.plot(x, y2, label='Our prediction', marker='o')
    plt.title(f'Evolution of {coin}', fontsize=15, fontweight='bold')
    plt.legend()
    plt.tight_layout()


frames = np.arange(250)

ani = FuncAnimation(plt.gcf(), animate, frames=frames, interval=100)
ani.save(f'./visu/animation_{name}.gif')

plt.tight_layout()
plt.show()

