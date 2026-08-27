use std::str::FromStr;

use pyo3::{pyfunction, PyResult};
use xid::Id;

use crate::errors::{bytes_parse_err, str_parse_err, XIDError};
use crate::wrapper::XID;

/// Parse the 20-character base32-hex representation of an XID.
pub(crate) fn parse_str(value: &str) -> PyResult<Id> {
    Id::from_str(value).map_err(|error| str_parse_err(&error, value))
}

/// Parse the 12-byte binary representation of an XID.
pub(crate) fn parse_bytes(value: &[u8]) -> PyResult<Id> {
    Id::from_bytes(value).map_err(|_| bytes_parse_err(value.len()))
}

/// Generate a new XID.
///
/// The generated ID embeds the current time, so a system clock set before the
/// Unix epoch makes generation impossible.
#[pyfunction]
pub fn xid_create() -> PyResult<XID> {
    // `xid::new` panics when the clock predates the Unix epoch; without this a
    // `PanicException` (a `BaseException`) would escape past `except Exception`.
    std::panic::catch_unwind(xid::new).map(XID).map_err(|_| {
        XIDError::new_err("cannot generate an XID: the system clock is set before the Unix epoch")
    })
}

/// Create an XID from its 20-character string representation.
#[pyfunction]
pub fn xid_from_str(s: &str) -> PyResult<XID> {
    parse_str(s).map(XID)
}

/// Create an XID from its 12-byte binary representation.
#[pyfunction]
pub fn xid_from_bytes(b: &[u8]) -> PyResult<XID> {
    parse_bytes(b).map(XID)
}
