#!/usr/bin/env bash
set -euo pipefail

req_bins=(git curl jq awk sed grep cut sort uniq head tail date)
echo "Validating required tools..."
for b in "${req_bins[@]}"; do
  if ! command -v "$b" >/dev/null 2>&1; then
    echo "Missing: $b"
  else
    echo -n "$b: "; "$b" --version 2>/dev/null | head -n1 || echo "ok"
  fi
done
echo "Done."
