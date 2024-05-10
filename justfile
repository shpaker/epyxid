#!/usr/bin/env just --justfile

build:
  maturin build \
    --find-interpreter

venv:
  source venv/bin/activate

tests:
  maturin develop
  set -e
  python3.8 -m pip install pytest
  python3.8 -m pytest -v test_xid.py
