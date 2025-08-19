# Linux QA Utilities — Pages with Charts

Adds **daily GitHub Pages publishing** *with charts* visualizing error trends over time.

This package assumes your server generates daily summaries in `/var/log/qa-summaries/summary-YYYY-MM-DD.log`
(using your existing `qa-log-summary.service/timer`). The GitHub Action securely copies them,
publishes to **gh-pages**, and renders **time-series charts** (PNG) plus a CSV.

## What’s new
- `github-pages/build_charts.py` parses `docs/logs/*.log`, counts ERROR/WARN/CRITICAL per day,
  writes `docs/charts/summary_counts.csv` and PNG charts.
- Updated workflow installs Python and runs the chart builder.
- `docs/index.html` is auto-regenerated with links to logs and embedded charts.

## Setup (recap)
1. Configure your server to generate `/var/log/qa-summaries/*.log` daily (systemd timer).
2. In this repo, set these Action secrets (Settings → Secrets and variables → Actions → New repository secret):
   - `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`, `REMOTE_LOG_DIR` (e.g., `/var/log/qa-summaries`)
   - optional: `SSH_PORT` (default 22)
3. Enable GitHub Pages: Settings → Pages → Source: Deploy from branch → Branch: `gh-pages`.

## Local dry-run
```bash
# simulate with example logs
python3 github-pages/build_charts.py docs/logs docs/charts
# open docs/index.html
```

## Notes
- Chart builder is defensive: if your log format isn’t known, it simply counts keyword occurrences
  (case-insensitive) for: `CRITICAL`, `ERROR`, `WARN` (and `WARNING`). Add more terms in the script if needed.
