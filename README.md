# ePyXID

[![PyPI](https://img.shields.io/pypi/v/epyxid.svg)](https://pypi.python.org/pypi/epyxid)
[![PyPI](https://img.shields.io/pypi/dm/epyxid.svg)](https://pypi.python.org/pypi/epyxid)

Fast globally unique sortable id generator.

Python wrapper around Rust implementation of xid https://github.com/kazk/xid-rs

## Install

```shell
pip install epyxid
```

## Usage

```python
from epyxid import XID

xid: XID = XID()
print(xid)
# cnisffq7qo0qnbtbu5gg
print(bytes(xid))
# b'e\xe5\xc7\xbfG\xd6\x01\xab\xaf\xab\xf1a'
print(xid.time)
# 2024-03-04 16:08:15
```
