import folium
import pandas as pd
import random

df = pd.read_csv("data/energy_log.csv")
latest = df.groupby("bin_id").tail(1)

city_lat = 26.8467
city_lon = 80.9462

m = folium.Map(location=[city_lat, city_lon], zoom_start=13)

for i, row in latest.iterrows():

    lat = city_lat + random.uniform(-0.03, 0.03)
    lon = city_lon + random.uniform(-0.03, 0.03)

    color = "green"
    if row["fill"] > 80:
        color = "red"
    elif row["fill"] > 50:
        color = "orange"

    folium.Marker(
        [lat, lon],
        popup=f"Bin {row['bin_id']} - {row['fill']}%",
        icon=folium.Icon(color=color)
    ).add_to(m)

m.save("outputs/smart_city_map.html")

print("Map Ready: outputs/smart_city_map.html")