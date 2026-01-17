# ePyXID

[![PyPI](https://img.shields.io/pypi/v/epyxid.svg)](https://pypi.python.org/pypi/epyxid)
[![PyPI](https://img.shields.io/pypi/dm/epyxid.svg)](https://pypi.python.org/pypi/epyxid)

Fast, globally unique, and sortable ID generator.

ePyXID is a Python wrapper around the Rust implementation of xid: [xid-rs](https://github.com/kazk/xid-rs). Built with [PyO3](https://pyo3.rs/), it provides a simple and efficient way to generate unique IDs that are sortable by creation time.

The original xid implementation is [rs/xid](https://github.com/rs/xid) written in Go.

## Features

- **Globally Unique**: Each ID is unique across space and time.
- **Sortable**: IDs are sortable by their creation time.
- **Fast**: Implemented in Rust for maximum performance using PyO3. See [performance benchmarks](https://github.com/shpaker/python-id-benchmarks) comparing ePyXID with other Python ID generation libraries.

## Installation

Install ePyXID using pip:

```shell
pip install epyxid
```

## Quick Start

Generate and use ePyXID in your Python projects:

```python
from epyxid import XID

# Create a new XID
xid = XID()
print(f"{xid!r}")
# <XID: cu701mcr9ij74n2hajpg>

# Create an XID from a string
xid_str = XID("cnisffq7qo0qnbtbu5gg")
print(f"XID from string: {xid_str}")

# Create an XID from bytes
xid_bytes = XID(b'e\xe5\xc7\xbfG\xd6\x01\xab\xaf\xab\xf1a')
print(f"XID from bytes: {xid_bytes}")

# Print the XID as a string
print(f"XID: {str(xid)}")
#  or
print(f"XID: {xid.to_str()}")
# XID: cnisffq7qo0qnbtbu5gg

# Get the byte representation of the XID
print(f"Bytes: {bytes(xid)}")
# or
print(f"Bytes: {xid.as_bytes()}")
# Bytes: b'e\xe5\xc7\xbfG\xd6\x01\xab\xaf\xab\xf1a'

# Access the creation time of the XID
print(f"Creation Time: {xid.time}")
# Creation Time: 2024-12-31 23:59:59

# Compare XIDs
xid1 = XID()
xid2 = XID()
print(f"XID1 < XID2: {xid1 < xid2}")

# Use XIDs in a set
xid_set = {xid1, xid2}
print(f"XID Set: {xid_set}")
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.
