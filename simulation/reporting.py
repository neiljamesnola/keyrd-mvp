import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

EXPORT_DIR = "export"
os.makedirs(EXPORT_DIR, exist_ok=True)

def generate_user_report(user_id):
    # Load and filter log
    df = pd.read_csv("nudge_decision_log.csv", header=None)
    df.columns = ["timestamp", "user_id", "arm", "reward", "engagement", "c1", "c2", "c3", "c4", "c5"]
    df = df[df["user_id"] == user_id]

    if df.empty:
        raise ValueError("No data found for user.")

    # Write CSV
    csv_path = os.path.join(EXPORT_DIR, f"user_summary_{user_id}.csv")
    df.to_csv(csv_path, index=False)

    # Summary stats
    stats = {
        "Total Nudges": len(df),
        "Mean Reward": round(df["reward"].mean(), 3),
        "Mean Engagement": round(df["engagement"].mean(), 3),
        "Estimated Dropout Risk": round((df["engagement"] < 0.3).mean(), 3)
    }

    # Generate plot
    fig, ax = plt.subplots(figsize=(8, 4))
    df["engagement"].plot(label="Engagement", ax=ax)
    df["reward"].plot(label="Reward", ax=ax)
    ax.set_title("User Engagement & Reward Over Time")
    ax.set_xlabel("Interaction")
    ax.set_ylabel("Value")
    ax.legend()
    plot_path = os.path.join(EXPORT_DIR, f"user_plot_{user_id}.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    # Generate PDF
    pdf_path = os.path.join(EXPORT_DIR, f"user_summary_{user_id}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"User Report: {user_id}", ln=True)

    for key, value in stats.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.image(plot_path, x=10, y=None, w=180)
    pdf.output(pdf_path)

    return {
        "csv": csv_path,
        "pdf": pdf_path
    }
