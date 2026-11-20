#!/usr/bin/env bash
set -eu
mkdir -p zap-output
chmod a+w zap-output

status=0
docker run --rm \
  -v "$PWD/zap-output:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t 'https://g1axy.github.io/bitcoin-order-app/' \
    -r zap_baseline_report.html || status=$?

if [ "$status" -gt 2 ]; then
  exit "$status"
fi

test -s zap-output/zap_baseline_report.html