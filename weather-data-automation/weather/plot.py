import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

METRIC_MAP = {
    "temperature": ("temperature_c", "Temperature (°C)", "Temperature (°C)"),
    "humidity": ("relative_humidity", "Relative Humidity (%)", "Rel. Humidity (%)"),
    "precipitation": ("precipitation_mm", "Precipitation (mm)", "Precipitation (mm)")
}

def _read_df(db_path: str):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM readings ORDER BY ts_utc", conn, parse_dates=["ts_utc"])
    conn.close()
    return df

def _aggregate_df(df: pd.DataFrame, aggregate: str):
    if aggregate == "daily":
        df = df.set_index("ts_utc").resample("D").mean(numeric_only=True).reset_index()
    return df

def plot_all(db_path: str, output_dir: str, metrics=None, aggregate: str = "hourly"):
    os.makedirs(output_dir, exist_ok=True)
    df = _read_df(db_path)
    if df.empty:
        print("No data found to plot.")
        return

    df = _aggregate_df(df, aggregate)
    selected = metrics or ["temperature", "humidity", "precipitation"]

    for m in selected:
        if m not in METRIC_MAP:
            print(f"Unknown metric '{m}', skipping.")
            continue
        col, title, ylabel = METRIC_MAP[m]
        if col not in df.columns:
            print(f"Column '{col}' missing, skipping metric '{m}'.")
            continue

        plt.figure()
        plt.plot(df["ts_utc"], df[col])
        plt.title(f"{title} over Time ({aggregate})")
        plt.xlabel("Time (UTC)")
        plt.ylabel(ylabel)
        plt.tight_layout()
        suffix = "_daily" if aggregate == "daily" else "_hourly"
        out_path = os.path.join(output_dir, f"{m}{suffix}.png")
        plt.savefig(out_path, dpi=140)
        plt.close()
        print(f"Saved: {out_path}")
