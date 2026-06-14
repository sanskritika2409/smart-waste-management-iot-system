from flask import Flask, render_template_string, jsonify
import pandas as pd

app = Flask(__name__)

# =========================
# HTML DASHBOARD (ADVANCED)
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Waste Advanced Dashboard</title>

    <meta http-equiv="refresh" content="5">

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
    /* =========================
   MOBILE RESPONSIVE DESIGN
========================= */

@media (max-width: 768px) {

    .header {
        font-size: 18px;
        padding: 15px;
    }

    .cards {
        grid-template-columns: 1fr;
    }

    table {
        font-size: 12px;
    }

    th, td {
        padding: 8px;
    }

    .chart-box {
        padding: 10px;
    }
}


        body {
            margin: 0;
            font-family: 'Inter', sans-serif;
            background: #0b0f19;
            color: white;
        }

        .header {
            padding: 20px;
            text-align: center;
            background: #111827;
            font-size: 24px;
            font-weight: 600;
        }

        .container {
            padding: 20px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .card {
            background: #1f2937;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
        }

        .green { color: #22c55e; }
        .orange { color: #f59e0b; }
        .red { color: #ef4444; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: #111827;
            border-radius: 10px;
            overflow: hidden;
        }

        th, td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #1f2937;
        }

        th {
            background: #1f2937;
        }

        .badge {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
        }

        .high { background: #ef4444; }
        .mid { background: #f59e0b; }
        .low { background: #22c55e; }

        /* Chart box */
        .chart-box {
            background: #1f2937;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }

    </style>
</head>

<body>

<div class="header">
    🚮 Smart Waste Management System (IoT Dashboard)
</div>

<div class="container">

    <!-- CARDS -->
    <div class="cards">
        <div class="card">
            <h3>Total Bins</h3>
            <h2>{{ total_bins }}</h2>
        </div>

        <div class="card">
            <h3>Critical</h3>
            <h2 class="red">{{ critical }}</h2>
        </div>

        <div class="card">
            <h3>Moderate</h3>
            <h2 class="orange">{{ moderate }}</h2>
        </div>

        <div class="card">
            <h3>Safe</h3>
            <h2 class="green">{{ safe }}</h2>
        </div>
    </div>

    <!-- CHART -->
    <div class="chart-box">
        <canvas id="binChart"></canvas>
    </div>

    <!-- TABLE -->
    <table>
        <tr>
            <th>Bin ID</th>
            <th>Distance</th>
            <th>Fill %</th>
            <th>Status</th>
        </tr>

        {% for row in data %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>

            <td>
                {% if row[3]|float > 80 %}
                    <span class="badge high">FULL</span>
                {% elif row[3]|float > 50 %}
                    <span class="badge mid">MEDIUM</span>
                {% else %}
                    <span class="badge low">EMPTY</span>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>

</div>

<script>

async function loadChart() {
    const res = await fetch("/chart-data");
    const data = await res.json();

    const ctx = document.getElementById('binChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.bins,
            datasets: [{
                label: 'Fill Level %',
                data: data.fill,
                backgroundColor: data.fill.map(v =>
                    v > 80 ? '#ef4444' :
                    v > 50 ? '#f59e0b' : '#22c55e'
                )
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

loadChart();
setInterval(loadChart, 5000);

</script>

</body>
</html>
"""

# =========================
# DASHBOARD ROUTE
# =========================
@app.route("/")
def dashboard():
    try:
        df = pd.read_csv("data/energy_log.csv")
    except:
        df = pd.DataFrame(columns=["bin_id","timestamp","distance","fill","status","priority"])

    latest = df.groupby("bin_id").tail(1)

    total_bins = len(latest)
    critical = len(latest[latest["fill"] > 80])
    moderate = len(latest[(latest["fill"] > 50) & (latest["fill"] <= 80)])
    safe = len(latest[latest["fill"] <= 50])

    return render_template_string(
        HTML,
        data=latest.values.tolist(),
        total_bins=total_bins,
        critical=critical,
        moderate=moderate,
        safe=safe
    )

# =========================
# CHART API
# =========================
@app.route("/chart-data")
def chart_data():
    df = pd.read_csv("data/energy_log.csv")
    df = df.groupby("bin_id").tail(1)

    return jsonify({
        "bins": df["bin_id"].tolist(),
        "fill": df["fill"].tolist()
    })

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)