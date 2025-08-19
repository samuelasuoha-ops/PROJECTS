#!/usr/bin/env bash
set -euo pipefail

# Ensure docs dirs exist
mkdir -p docs/logs docs/charts

# Copy all logs from working directory (already downloaded by the workflow)
# Expecting logs in ./_downloaded_logs
if [ -d "_downloaded_logs" ]; then
  cp -f _downloaded_logs/*.log docs/logs/ || true
fi

# Generate index and charts
python3 github-pages/build_charts.py docs/logs docs/charts
