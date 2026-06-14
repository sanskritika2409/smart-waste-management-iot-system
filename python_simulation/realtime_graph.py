import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("ggplot")

def animate(i):
    df = pd.read_csv("data/energy_log.csv")

    if len(df) < 5:
        return

    df = df.tail(50)

    plt.cla()
    plt.plot(df["fill"], label="Fill Level %", color="blue")
    plt.title("🚮 Real-Time Smart Bin Fill Level")
    plt.xlabel("Time")
    plt.ylabel("Fill %")
    plt.ylim(0, 100)
    plt.legend()

ani = FuncAnimation(plt.gcf(), animate, interval=2000)

plt.tight_layout()
plt.show()