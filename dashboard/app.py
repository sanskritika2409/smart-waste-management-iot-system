from flask import Flask, render_template_string
import csv

app = Flask(__name__)

HTML = """
<h1>Smart Waste Dashboard</h1>
<table border="1">
<tr><th>Time</th><th>Distance</th><th>Fill</th><th>Status</th></tr>
{% for row in data %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
<td>{{row[3]}}</td>
</tr>
{% endfor %}
</table>
"""

@app.route("/")
def home():
    data = []
    try:
        with open("../data/energy_log.csv") as f:
            reader = csv.reader(f)
            next(reader)
            data = list(reader)
    except:
        data = []

    return render_template_string(HTML, data=data)

if __name__ == "__main__":
    app.run(debug=True)
