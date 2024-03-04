#!/usr/bin/env just --justfile
#export PYO3_PRINT_CONFIG:="1"

build:
  maturin build \
    --interpreter python3.8

tests:
  maturin develop
  pytest -v test_xid.py
