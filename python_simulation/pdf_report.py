from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime

def generate_pdf():
    df = pd.read_csv("../data/energy_log.csv")

    file_name = "../reports/waste_report.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, 750, "Smart Waste Management Report")

    c.setFont("Helvetica", 10)
    y = 720

    c.drawString(50, y, "Bin Monitoring Summary:")
    y -= 20

    for i in range(min(20, len(df))):
        row = df.iloc[i]
        text = f"Bin {row['bin_id']} | Fill: {row['fill']}% | Status: {row['status']}"
        c.drawString(50, y, text)
        y -= 15

        if y < 50:
            c.showPage()
            y = 750

    c.save()
    print("PDF Generated:", file_name)

if __name__ == "__main__":
    generate_pdf()