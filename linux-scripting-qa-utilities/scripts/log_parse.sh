#!/usr/bin/env bash
set -euo pipefail

FILE=""
TOP=10
USE_JOURNAL=0
JOURNAL_UNIT=""
CONFIG=""

usage() {
  cat <<EOF
Usage:
  $0 --file path [--top N]
  $0 --journal --unit SERVICE [--top N]
  $0 --config config/summary.conf
EOF
}

# Read config file: simple KEY=VALUE pairs
load_config() {
  local cfg="$1"
  if [[ ! -f "$cfg" ]]; then
    echo "Config not found: $cfg" >&2
    exit 1
  fi
  # shellcheck disable=SC1090
  source "$cfg"
  # Expected variables:
  # LOG_SOURCE: "file" or "journal"
  # LOG_FILE: path when LOG_SOURCE=file
  # JOURNAL_UNIT: systemd unit when LOG_SOURCE=journal
  # PATTERN: e.g. "ERROR|WARN|CRITICAL"
  # OUTPUT_DIR: e.g. "/var/log/qa-summaries"
  FILE="${LOG_FILE:-}"
  JOURNAL_UNIT="${JOURNAL_UNIT:-}"
  PATTERN="${PATTERN:-ERROR|WARN|CRITICAL}"
  OUTPUT_DIR="${OUTPUT_DIR:-/var/log/qa-summaries}"
  mkdir -p "$OUTPUT_DIR"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift 2 ;;
    --top) TOP="$2"; shift 2 ;;
    --journal) USE_JOURNAL=1; shift ;;
    --unit) JOURNAL_UNIT="$2"; shift 2 ;;
    --config) CONFIG="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

if [[ -n "$CONFIG" ]]; then
  load_config "$CONFIG"
fi

today="$(date +%F)"
out="${OUTPUT_DIR:-./}/summary-${today}.log"

echo "# QA Log Summary - ${today}" > "$out"
echo "# Host: $(hostname)  UTC: $(date -u +"%F %T")" >> "$out"
echo >> "$out"

# Choose source
if [[ $USE_JOURNAL -eq 1 || "${LOG_SOURCE:-}" == "journal" ]]; then
  if [[ -z "${JOURNAL_UNIT:-}" ]]; then
    echo "Missing --unit or JOURNAL_UNIT" >&2; exit 1
  fi
  echo "Source: systemd journal (${JOURNAL_UNIT})" >> "$out"
  # Last day
  journalctl -u "$JOURNAL_UNIT" --since "24 hours ago" --no-pager | tee /dev/stderr | \
    awk '{print $0}' > /tmp/qa_lines.$$
else
  if [[ -z "$FILE" ]]; then
    echo "Missing --file path" >&2; exit 1
  fi
  echo "Source: file ($FILE)" >> "$out"
  tail -n 50000 "$FILE" > /tmp/qa_lines.$$
fi

echo >> "$out"
echo "## Top ${TOP} IPs / Sources" >> "$out"
awk '{for(i=1;i<=2;i++){ if ($i ~ /[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/) print $i }}' /tmp/qa_lines.$$ | \
  sort | uniq -c | sort -rn | head -n "$TOP" >> "$out"

echo >> "$out"
echo "## Status / Levels" >> "$out"
grep -E -o "${PATTERN:-ERROR|WARN|CRITICAL}| [1-5][0-9][0-9] " /tmp/qa_lines.$$ | \
  sed 's/^ *//' | sort | uniq -c | sort -rn | head -n "$TOP" >> "$out"

echo >> "$out"
echo "## Top ${TOP} Endpoints" >> "$out"
grep -E -o '"(GET|POST|PUT|DELETE|PATCH) [^"]+' /tmp/qa_lines.$$ | \
  cut -d' ' -f2 | sort | uniq -c | sort -rn | head -n "$TOP" >> "$out"

rm -f /tmp/qa_lines.$$

echo >> "$out"
echo "Wrote summary to $out"
echo "$out"
