#!/usr/bin/env just --justfile
#export PYO3_PRINT_CONFIG:="1"

build:
  maturin build \
    --interpreter python3.8 \
    --release
#    --target-dir xid-wrapper \
#    --out _wheels

#  poetry run pip install _wheels/epyxid-0.1.0-cp38-cp38-macosx_11_0_arm64.whl
