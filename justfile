#!/usr/bin/env just --justfile

venv:
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade "maturin>=1.9,<2.0" "pytest>=8.3" mypy

tests:
  rm -rf target/wheels
  maturin build --locked --out target/wheels
  python -m pip install --no-index --force-reinstall target/wheels/epyxid-*.whl
  python -m pytest -v test_xid.py

stubs:
  python -m mypy epyxid.pyi
  python -m mypy.stubtest epyxid --ignore-missing-stub

lint:
  cargo fmt --check
  cargo clippy --all-targets --locked -- -D warnings

hooks:
  prek install

hooks-run:
  prek run --all-files
