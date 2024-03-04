use std::str::FromStr;

use pyo3::types::PyBytes;
use pyo3::{pyfunction, PyResult};
use xid::{Id, ParseIdError};

use crate::errors::XIDError;
use crate::wrapper::XID;

#[pyfunction]
pub fn xid_create() -> PyResult<XID> {
    Ok(XID { inner: xid::new() })
}

#[pyfunction]
pub fn xid_from_str(s: &str) -> PyResult<XID> {
    match Id::from_str(s) {
        Ok(id) => Ok(XID { inner: id }),
        Err(error) => Err(XIDError::new_err(error.to_string())),
    }
}

#[pyfunction]
pub fn xid_from_bytes(b: &PyBytes) -> PyResult<XID> {
    match id_from_bytes(b.as_bytes()) {
        Ok(value) => Ok(XID { inner: value }),
        Err(error) => Err(XIDError::new_err(error.to_string())),
    }
}

fn id_from_bytes(s: &[u8]) -> Result<Id, ParseIdError> {
    if s.len() != 12 {
        return Err(ParseIdError::InvalidLength(s.len()));
    }
    let value = unsafe { &*(s as *const [u8] as *const [u8; 12]) };
    Ok(Id(*value))
}
