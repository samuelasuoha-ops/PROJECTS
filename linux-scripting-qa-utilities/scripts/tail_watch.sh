#!/usr/bin/env bash
set -euo pipefail

FILE=""
PATTERN="ERROR|WARN|CRITICAL"
USE_JOURNAL=0
UNIT=""

usage() {
  cat <<EOF
Usage:
  $0 --file /var/log/syslog [--pattern "ERROR|WARN"]
  $0 --journal --unit nginx.service [--pattern "5..|error"]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift 2 ;;
    --pattern) PATTERN="$2"; shift 2 ;;
    --journal) USE_JOURNAL=1; shift ;;
    --unit) UNIT="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

color() { tput setaf "$1" 2>/dev/null || true; }
reset() { tput sgr0 2>/dev/null || true; }

highlight() {
  perl -pe 'BEGIN{$|=1;} s/('"$PATTERN"')/"\e[1;31m$1\e[0m"/gi'
}

if [[ $USE_JOURNAL -eq 1 ]]; then
  [[ -z "$UNIT" ]] && { echo "Missing --unit"; exit 1; }
  journalctl -f -u "$UNIT" --no-pager | highlight
else
  [[ -z "$FILE" ]] && { echo "Missing --file"; exit 1; }
  tail -F "$FILE" | highlight
fi
