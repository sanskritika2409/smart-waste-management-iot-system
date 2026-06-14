import pandas as pd

def check_alerts():
    df = pd.read_csv("../data/energy_log.csv")

    alerts = df[df["fill"] > 80]

    print("\n🚨 ALERT SYSTEM")
    print("-" * 30)

    if alerts.empty:
        print("No alerts")
    else:
        for _, row in alerts.iterrows():
            print(f"Bin {row['bin_id']} FULL at {row['fill']}%")

if __name__ == "__main__":
    check_alerts()