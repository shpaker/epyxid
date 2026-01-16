#!/usr/bin/env just --justfile

venv:
  source venv/bin/activate

tests:
  maturin build --out dist --interpreter python
  python -m pip install --no-index --find-links dist/ --force-reinstall epyxid
  python -m pip install pytest
  python -m pytest -v test_xid.py
