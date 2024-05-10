#!/usr/bin/env just --justfile

venv:
  source venv/bin/activate

tests:
  maturin build --out dist --interpreter python
  python3.8 -m pip install --no-index --find-links dist/ --force-reinstall epyxid
  python3.8 -m pip install pytest
  python3.8 -m pytest -v test_xid.py
