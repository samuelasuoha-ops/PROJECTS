#!/usr/bin/env bash
set -euo pipefail

EXPECTED_FILE=""
EXPECTED_STR=""
CMD=""
IGNORE_CASE=0
STRIP_WS=0

usage() {
  cat <<EOF
Usage: $0 --cmd "<command>" [--expected "<text>" | --expected-file path] [--ignore-case] [--strip-trailing-ws]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cmd) CMD="$2"; shift 2 ;;
    --expected) EXPECTED_STR="$2"; shift 2 ;;
    --expected-file) EXPECTED_FILE="$2"; shift 2 ;;
    --ignore-case) IGNORE_CASE=1; shift ;;
    --strip-trailing-ws) STRIP_WS=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$CMD" ]]; then
  echo "Missing --cmd"; usage; exit 1
fi

OUTPUT="$(bash -c "$CMD")"

tmp_expected=$(mktemp)
if [[ -n "$EXPECTED_FILE" ]]; then
  cat "$EXPECTED_FILE" > "$tmp_expected"
elif [[ -n "$EXPECTED_STR" ]]; then
  printf "%s\n" "$EXPECTED_STR" > "$tmp_expected"
else
  echo "Provide --expected or --expected-file"; exit 1
fi

tmp_out=$(mktemp)
printf "%s\n" "$OUTPUT" > "$tmp_out"

diff_flags="-u"
[[ $IGNORE_CASE -eq 1 ]] && diff_flags="$diff_flags -i"
[[ $STRIP_WS -eq 1 ]] && { sed -i 's/[[:space:]]\+$//' "$tmp_expected"; sed -i 's/[[:space:]]\+$//' "$tmp_out"; }

if diff $diff_flags "$tmp_expected" "$tmp_out"; then
  echo "OK"
  exit 0
else
  echo "FAILED"
  exit 2
fi
