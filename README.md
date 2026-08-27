# ePyXID

[![PyPI version](https://img.shields.io/pypi/v/epyxid.svg)](https://pypi.org/project/epyxid/)
[![PyPI downloads](https://img.shields.io/pypi/dm/epyxid.svg)](https://pypi.org/project/epyxid/)

Fast, globally unique, and sortable ID generator.

ePyXID is a Python wrapper around the Rust implementation of xid: [xid-rs](https://github.com/kazk/xid-rs). Built with [PyO3](https://pyo3.rs/), it provides a simple and efficient way to generate unique IDs that are sortable by creation time.

The original xid implementation is [rs/xid](https://github.com/rs/xid) written in Go.

## Features

- **Globally Unique**: Each ID combines a timestamp, a machine identifier, a process identifier and a counter.
- **Sortable**: IDs sort by creation time with one-second granularity.
- **Compact**: 12 bytes, or 20 characters in its base32-hex form.
- **Fast**: Implemented in Rust for maximum performance using PyO3. See [performance benchmarks](https://github.com/shpaker/python-id-benchmarks) comparing ePyXID with other Python ID generation libraries.
- **Typed**: Ships type stubs and `py.typed`.

## Installation

Requires Python 3.10 or newer.

```shell
pip install epyxid
```

## Quick Start

```python
from epyxid import XID, XIDError

# Generate a new ID
xid = XID()
print(repr(xid))
print(xid.time)

# Parse an existing ID from its string or binary form
from_str = XID('9m4e2mr0ui3e8a215n4g')
from_bytes = XID(b'\x4d\x88\xe1\x5b\x60\xf4\x86\xe4\x28\x41\x2d\xc9')
print(from_str == from_bytes)
# True

# Convert back
print(from_str.to_str())
# 9m4e2mr0ui3e8a215n4g
print(from_str.as_bytes())
# b'M\x88\xe1[`\xf4\x86\xe4(A-\xc9'

# Inspect the embedded fields
print(from_str.machine, from_str.pid, from_str.counter)
# b'`\xf4\x86' 58408 4271561

# IDs are ordered, hashable and picklable
print(XID() < XID())
# True
print(len({from_str, from_bytes}))
# 1

# Invalid input raises XIDError, a subclass of ValueError
try:
    XID('not-an-xid')
except XIDError as error:
    print(error)
# invalid XID string "not-an-xid": expected 20 characters, got 10
```

Only `str` and `bytes` are accepted; anything else raises `TypeError`.

## Development

Requires a Rust toolchain, [just](https://github.com/casey/just) and [prek](https://github.com/j178/prek).

```shell
just venv    # create .venv with maturin, pytest and mypy
just hooks   # install git hooks
just tests   # build the wheel and run the test suite
just stubs   # type-check the stubs against the built module
just lint    # cargo fmt and clippy
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/shpaker/epyxid).

## License

This project is licensed under the MIT License.
