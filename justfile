#!/usr/bin/env just --justfile

build:
  maturin build \
    --interpreter python3.8

tests:
  maturin develop
  pytest -v test_xid.py
