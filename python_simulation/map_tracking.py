import pandas as pd
import folium
import random

df = pd.read_csv("data/energy_log.csv")

latest = df.groupby("bin_id").tail(1)

# Fake city center (Lucknow)
base_lat = 26.8467
base_lon = 80.9462

m = folium.Map(location=[base_lat, base_lon], zoom_start=13)

for i, row in latest.iterrows():

    lat = base_lat + random.uniform(-0.02, 0.02)
    lon = base_lon + random.uniform(-0.02, 0.02)

    color = "green"
    if row["fill"] > 80:
        color = "red"
    elif row["fill"] > 50:
        color = "orange"

    folium.Marker(
        location=[lat, lon],
        popup=f"Bin {row['bin_id']} | {row['fill']}%",
        icon=folium.Icon(color=color)
    ).add_to(m)

m.save("outputs/bin_map.html")

print("Map generated: outputs/bin_map.html")