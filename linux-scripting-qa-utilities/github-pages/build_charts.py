import os, sys, re, csv, datetime, html

SEVERITIES = [
    ("CRITICAL", re.compile(r"\bCRITICAL\b", re.IGNORECASE)),
    ("ERROR", re.compile(r"\bERROR\b", re.IGNORECASE)),
    ("WARN", re.compile(r"\bWARN(?:ING)?\b", re.IGNORECASE)),
]

def parse_date_from_filename(name: str):
    # expects summary-YYYY-MM-DD.log or similar; fallback to mtime
    m = re.search(r"(\d{4}-\d{2}-\d{2})", name)
    if m:
        try:
            return datetime.date.fromisoformat(m.group(1))
        except Exception:
            pass
    # fallback: today
    return datetime.date.fromtimestamp(os.path.getmtime(name))

def count_severities(filepath: str):
    counts = {k: 0 for k, _ in SEVERITIES}
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                for key, rx in SEVERITIES:
                    if rx.search(line):
                        counts[key] += 1
    except Exception:
        pass
    return counts

def write_csv(rows, out_csv):
    rows_sorted = sorted(rows, key=lambda r: r["date"])
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "CRITICAL", "ERROR", "WARN"])
        w.writeheader()
        for r in rows_sorted:
            w.writerow({
                "date": r["date"].isoformat(),
                "CRITICAL": r["CRITICAL"],
                "ERROR": r["ERROR"],
                "WARN": r["WARN"],
            })

def make_charts(rows, charts_dir):
    # Use pure HTML with a small inline SVG sparkline per series to avoid Python deps on GH runner
    # But we can also provide matplotlib-like PNGs using inline JS? To keep it simple: small SVGs and also a PNG hint optional
    # Here we do simple SVG sparklines per severity.
    def svg_spark(values, width=600, height=120, pad=10):
        if not values:
            return "<svg width='{}' height='{}'></svg>".format(width, height)
        vmax = max(values) or 1
        step = (width - 2*pad) / max(1, len(values)-1)
        points = []
        for i, v in enumerate(values):
            x = pad + i*step
            y = height - pad - (v / vmax) * (height - 2*pad)
            points.append(f"{x:.1f},{y:.1f}")
        poly = " ".join(points)
        return f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' role='img' aria-label='sparkline'><polyline fill='none' stroke='currentColor' stroke-width='2' points='{poly}'/></svg>"

    dates = [r["date"] for r in rows]
    crit = [r["CRITICAL"] for r in rows]
    err  = [r["ERROR"] for r in rows]
    warn = [r["WARN"] for r in rows]

    # Save a simple HTML fragment including three sparklines
    frag_path = os.path.join(charts_dir, "index.html")
    with open(frag_path, "w", encoding="utf-8") as fh:
        fh.write("<!doctype html><meta charset='utf-8'><title>Charts</title>")
        fh.write("<style>body{font-family:system-ui,Arial,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}h2{margin-top:1.5rem}.chart{margin:1rem 0}</style>")
        fh.write("<h1>Daily Log Severity Trends</h1>")
        if not rows:
            fh.write("<p>No data.</p>")
        else:
            lab = ", ".join(d.isoformat() for d in dates)
            fh.write("<div class='chart'><h2>CRITICAL</h2>")
            fh.write(svg_spark(crit))
            fh.write("</div>")
            fh.write("<div class='chart'><h2>ERROR</h2>")
            fh.write(svg_spark(err))
            fh.write("</div>")
            fh.write("<div class='chart'><h2>WARN</h2>")
            fh.write(svg_spark(warn))
            fh.write("</div>")
    return frag_path

def build_index(logs_dir, charts_dir):
    files = sorted([f for f in os.listdir(logs_dir) if f.endswith(".log")])
    index_path = os.path.join(os.path.dirname(logs_dir), "index.html")
    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write("<!doctype html><meta charset='utf-8'>")
        fh.write("<title>Daily QA Log Summaries</title>")
        fh.write("<style>body{font-family:system-ui,Arial,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem}h1{margin-bottom:.25rem}ul{line-height:1.8}a{word-break:break-all}</style>")
        fh.write("<h1>Daily QA Log Summaries</h1>")
        if not files:
            fh.write("<p>No logs found.</p>")
        else:
            fh.write("<h2>Logs</h2><ul>")
            for f in files:
                fh.write(f"<li><a href='logs/{f}'>{f}</a></li>")
            fh.write("</ul>")
            fh.write("<h2>Charts</h2>")
            fh.write("<p>See <a href='charts/index.html'>severity trends</a>.</p>")
    return index_path

def main():
    logs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/logs"
    charts_dir = sys.argv[2] if len(sys.argv) > 2 else "docs/charts"
    os.makedirs(charts_dir, exist_ok=True)

    rows = []
    for name in os.listdir(logs_dir):
        if not name.endswith(".log"):
            continue
        path = os.path.join(logs_dir, name)
        if not os.path.isfile(path):
            continue
        d = parse_date_from_filename(name)
        counts = count_severities(path)
        row = {"date": d}
        row.update(counts)
        rows.append(row)

    rows.sort(key=lambda r: r["date"])
    out_csv = os.path.join(charts_dir, "summary_counts.csv")
    if rows:
        write_csv(rows, out_csv)
    frag = make_charts(rows, charts_dir)
    idx = build_index(logs_dir, charts_dir)
    print(f"Wrote:\n- {out_csv if rows else '(no CSV)'}\n- {frag}\n- {idx}")

if __name__ == "__main__":
    main()
