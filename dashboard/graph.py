import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/energy_log.csv")

plt.plot(df["fill_percent"])
plt.title("Bin Fill Level Trend")
plt.xlabel("Time")
plt.ylabel("Fill %")
plt.show()
