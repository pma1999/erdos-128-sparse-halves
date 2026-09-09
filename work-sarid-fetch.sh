#!/bin/sh
# Fetches the third-party flag-algebra certificate referenced in
# outputs/density-split-certificate.md, instead of redistributing it.
# It belongs to its authors; this repository does not relicense it.
set -e
mkdir -p work/sarid-certificate
cd work/sarid-certificate
BASE="https://raw.githubusercontent.com/aimir/erdos-128-sparse-halves/main"
curl -fsSLO "$BASE/verify_clebsch_tangent_certificate.py"
curl -fsSLO "$BASE/clebsch_tangent_certificate.json"
echo "Fetched. Record the SHA-256 of each file before relying on it:"
sha256sum ./* 2>/dev/null || shasum -a 256 ./*
