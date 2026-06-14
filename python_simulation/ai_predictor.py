import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/energy_log.csv")

df = df.groupby("bin_id").tail(20)

X = np.array(range(len(df))).reshape(-1, 1)
y = df["fill"].values

model = LinearRegression()
model.fit(X, y)

next_time = np.array([[len(df)+5]])
prediction = model.predict(next_time)

print("📊 AI Prediction:")
print(f"Bin will reach ~{prediction[0]:.2f}% soon")