import argparse
import json
import os
from . import db, fetch, plot

def load_config(path: str):
    with open(path, "r") as f:
        cfg = json.load(f)
    base = os.path.dirname(os.path.abspath(path))
    cfg["db_path"] = os.path.abspath(os.path.join(base, cfg.get("db_path", "data/weather.db")))
    cfg["output_dir"] = os.path.abspath(os.path.join(base, cfg.get("output_dir", "output")))
    cfg["days"] = int(cfg.get("days", 3))
    return cfg

def cmd_fetch(cfg, days_override=None):
    db.init_db(cfg["db_path"])
    days = int(days_override) if days_override is not None else cfg["days"]
    hours = max(24, min(24*7, days * 24))
    rows = fetch.fetch_weather(cfg["latitude"], cfg["longitude"], hours_back=hours)
    db.upsert_readings(cfg["db_path"], rows)
    print(f"Fetched {len(rows)} hourly records")

def cmd_plot(cfg, metrics=None, aggregate='hourly'):
    plot.plot_all(cfg["db_path"], cfg["output_dir"], metrics=metrics, aggregate=aggregate)

def main():
    ap = argparse.ArgumentParser(description="Weather Data Automation — Unified")
    ap.add_argument("--config", default="config.json", help="Path to config.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_fetch = sub.add_parser("fetch", help="Fetch weather and store to SQLite")
    ap_fetch.add_argument("--days", type=int, help="Override days in config (1-7)")

    ap_plot = sub.add_parser("plot", help="Create charts from SQLite")
    ap_plot.add_argument("--aggregate", choices=["hourly", "daily"], default="hourly")
    ap_plot.add_argument("--metrics", type=str, help="Comma-separated metrics: temperature,humidity,precipitation")

    ap_all = sub.add_parser("all", help="Fetch then plot")
    ap_all.add_argument("--days", type=int, help="Override days in config (1-7)")
    ap_all.add_argument("--aggregate", choices=["hourly", "daily"], default="hourly")
    ap_all.add_argument("--metrics", type=str, help="Comma-separated metrics")

    args = ap.parse_args()
    cfg = load_config(args.config)

    if args.cmd == "fetch":
        cmd_fetch(cfg, days_override=args.days)
    elif args.cmd == "plot":
        metrics = args.metrics.split(",") if args.metrics else None
        cmd_plot(cfg, metrics=metrics, aggregate=args.aggregate)
    elif args.cmd == "all":
        metrics = args.metrics.split(",") if args.metrics else None
        cmd_fetch(cfg, days_override=args.days)
        cmd_plot(cfg, metrics=metrics, aggregate=args.aggregate)

if __name__ == "__main__":
    main()
