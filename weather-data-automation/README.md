# Weather Data Automation — Unified (Artifacts + GitHub Pages)

Automates fetching weather data from **Open-Meteo**, stores it in **SQLite**, and generates charts with **Matplotlib**.  
This unified repo includes two GitHub Actions:
- **Daily Scheduled Run (07:00 UTC)** → fetch & plot → **upload charts as artifacts**.
- **GitHub Pages Deploy** → fetch & plot → **publish charts to `gh-pages`** with an auto-generated index page.

**Tech:** Python, REST API, SQLite, Matplotlib, GitHub Actions, Cron-like schedule

## Quick Start (Local)
```bash
python -m venv .venv && source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp config.example.json config.json   # edit lat/lon if needed

# Fetch and plot hourly
python -m weather.cli all --config config.json

# Daily average charts for temperature + humidity only
python -m weather.cli plot --config config.json --aggregate daily --metrics temperature,humidity
```

Charts appear in `output/`. The SQLite DB is stored at `data/weather.db`.

## GitHub Actions
### 1) Daily Schedule (Artifacts)
- Workflow: `.github/workflows/schedule.yml`
- Runs daily at **07:00 UTC**
- Uploads `output/` as an **artifact**

### 2) GitHub Pages (Public Charts Only)
- Workflow: `.github/workflows/pages.yml`
- Also runs daily (07:00 UTC) or on demand
- **Publishes only `output/`** to the `gh-pages` branch
- **The SQLite database is NEVER published** to Pages

### Enable Pages
1. Push this repo to GitHub.
2. Go to **Settings → Pages**:
   - **Source**: *Deploy from a branch*
   - **Branch**: `gh-pages` (root)
3. Trigger the workflow or wait for 07:00 UTC.

Your site: `https://<username>.github.io/<repo>/`

## CLI
```
python -m weather.cli fetch --config config.json [--days 3]
python -m weather.cli plot  --config config.json [--aggregate hourly|daily] [--metrics temperature,humidity,precipitation]
python -m weather.cli all   --config config.json [--days 3] [--aggregate hourly|daily] [--metrics ...]
```

## Data Model
SQLite table `readings`:
- `ts_utc` (TEXT, ISO-8601, primary key)
- `temperature_c` (REAL)
- `relative_humidity` (REAL)
- `precipitation_mm` (REAL)

Generated 2025-08-18.
