import pandas as pd

def analyze():
    df = pd.read_csv("data/energy_log.csv")

    print("\n📊 SMART WASTE ANALYTICS")
    print("-" * 40)

    print("Total Records:", len(df))

    print("\nBin-wise Average Fill Level:")
    print(df.groupby("bin_id")["fill"].mean())

    print("\nBins Requiring Immediate Attention:")
    alert_bins = df[df["fill"] > 80]["bin_id"].unique()
    print(alert_bins)

    print("\nRoute Priority (High → Low):")
    route = df.sort_values(by="priority", ascending=False)[["bin_id", "fill", "priority"]]
    print(route.drop_duplicates())

if __name__ == "__main__":
    analyze()