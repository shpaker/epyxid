#!/usr/bin/env just --justfile

# Recipes use .venv so the pinned maturin is always the one that builds.
venv:
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade "maturin>=1.9,<2.0" "pytest>=8.3" mypy

tests:
  rm -rf target/wheels
  .venv/bin/maturin build --locked --out target/wheels
  .venv/bin/python -m pip install --no-index --force-reinstall target/wheels/epyxid-*.whl
  .venv/bin/python -m pytest -v test_xid.py

stubs:
  .venv/bin/python -m mypy epyxid.pyi
  .venv/bin/python -m mypy.stubtest epyxid --ignore-missing-stub

sdist:
  rm -rf target/sdist
  .venv/bin/maturin sdist --out target/sdist

hooks:
  prek install

hooks-run:
  prek run --all-files

lint:
  cargo fmt --check
  cargo clippy --all-targets --locked -- -D warnings
