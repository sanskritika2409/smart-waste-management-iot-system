import random
import time
import csv
import json
from datetime import datetime

BIN_HEIGHT = 30
NUM_BINS = 5

def generate_bin_data(bin_id):
    distance = random.uniform(2, 30)
    fill = 100 - (distance / BIN_HEIGHT * 100)
    fill = max(0, min(100, fill))

    if fill > 80:
        status = "FULL"
        priority = 3
    elif fill > 50:
        status = "MEDIUM"
        priority = 2
    else:
        status = "LOW"
        priority = 1

    return {
        "bin_id": bin_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "distance": round(distance, 2),
        "fill": round(fill, 2),
        "status": status,
        "priority": priority
    }

def run_simulation():
    with open("data/energy_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["bin_id", "timestamp", "distance", "fill", "status", "priority"])

        for _ in range(200):
            for bin_id in range(1, NUM_BINS + 1):
                data = generate_bin_data(bin_id)

                writer.writerow([
                    data["bin_id"],
                    data["timestamp"],
                    data["distance"],
                    data["fill"],
                    data["status"],
                    data["priority"]
                ])

                print(json.dumps(data))

            time.sleep(1)

if __name__ == "__main__":
    run_simulation()