#!/usr/bin/env bash
status=0
npx --yes --package=jshint@2.13.6 -- jshint --exclude=node_modules/ --reporter=unix . > JSHint-report 2>&1 || status=$?

if [ "$status" -eq 0 ] && [ ! -s JSHint-report ]; then
  echo "JSHint completed with no findings." > JSHint-report
fi

if [ "$status" -ne 0 ] && [ "$status" -ne 2 ]; then
  cat JSHint-report
  exit "$status"
fi