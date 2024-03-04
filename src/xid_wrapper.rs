use pyo3::{pyclass, pymethods, PyResult, Python};
use xid::Id;
use pyo3::types::{PyBytes, PyDateTime};
use std::str::FromStr;
use crate::XIDError;

const RAW_LEN: usize = 12;

#[pyclass]
pub struct XID {
    inner: Id,
}

#[pymethods]
impl XID {
    #[staticmethod]
    fn create() -> PyResult<XID> {
        Ok(XID { inner: xid::new() })
    }

    #[staticmethod]
    fn from_str(s: &str) -> PyResult<XID> {
        match Id::from_str(s) {
            Ok(id) => Ok(XID { inner: id }),
            Err(error) => Err(XIDError::new_err(error.to_string())),
        }
    }

    fn as_bytes<'p>(&self, _py: Python<'p>) -> &'p PyBytes {
        PyBytes::new(_py, self.inner.as_bytes())
    }

    fn as_str(&self) -> String {
        self.inner.to_string()
    }

    fn machine<'p>(&self, _py: Python<'p>) -> &'p PyBytes {
        PyBytes::new(_py, &self.inner.machine())
    }

    fn pid(&self) -> u16 {
        self.inner.pid()
    }

    fn time<'p>(&self, _py: Python<'p>) -> PyResult<&'p PyDateTime> {
        let raw = self.inner.as_bytes();
        let unix_ts = u32::from_be_bytes([raw[0], raw[1], raw[2], raw[3]]);
        PyDateTime::from_timestamp(_py, unix_ts as f64, None)
    }

    fn counter(&self) -> u32 {
        self.inner.counter()
    }

    fn __str__(&self) -> String {
        self.as_str()
    }

    fn __repr__(&self) -> String {
        format!("<XID: {}>", self.as_str())
    }

    fn __eq__(&self, object: &XID) -> bool {
        self.as_str() == object.as_str()
    }

    fn __ne__(&self, object: &XID) -> bool {
        self.as_str() != object.as_str()
    }

    fn __lt__(&self, object: &XID) -> bool {
        self.as_str() < object.as_str()
    }

    fn __le__(&self, object: &XID) -> bool {
        self.as_str() <= object.as_str()
    }

    fn __gt__(&self, object: &XID) -> bool {
        self.as_str() > object.as_str()
    }

    fn __ge__(&self, object: &XID) -> bool {
        self.as_str() >= object.as_str()
    }
}
