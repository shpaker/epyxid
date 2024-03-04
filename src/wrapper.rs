use std::str::FromStr;

use pyo3::types::{PyBytes, PyDateTime};
use pyo3::{pyclass, pymethods, PyResult, Python};
use xid::Id;

#[pyclass]
pub struct XID {
    pub inner: Id,
}

#[pymethods]
impl XID {
    fn as_bytes<'p>(&self, _py: Python<'p>) -> &'p PyBytes {
        PyBytes::new(_py, self.inner.as_bytes())
    }

    fn to_str(&self) -> String {
        self.inner.to_string()
    }

    #[getter]
    fn machine<'p>(&self, _py: Python<'p>) -> &'p PyBytes {
        PyBytes::new(_py, &self.inner.machine())
    }

    #[getter]
    fn pid(&self) -> u16 {
        self.inner.pid()
    }

    #[getter]
    fn time<'p>(&self, _py: Python<'p>) -> PyResult<&'p PyDateTime> {
        let raw = self.inner.as_bytes();
        let unix_ts = u32::from_be_bytes([raw[0], raw[1], raw[2], raw[3]]);
        PyDateTime::from_timestamp(_py, unix_ts as f64, None)
    }

    #[getter]
    fn counter(&self) -> u32 {
        self.inner.counter()
    }

    fn __bytes__<'p>(&self, _py: Python<'p>) -> &'p PyBytes {
        self.as_bytes(_py)
    }

    fn __str__(&self) -> String {
        self.to_str()
    }

    fn __repr__(&self) -> String {
        format!("<XID: {}>", self.to_str())
    }

    fn __eq__(&self, object: &XID) -> bool {
        self.to_str() == object.to_str()
    }

    fn __ne__(&self, object: &XID) -> bool {
        self.to_str() != object.to_str()
    }

    fn __lt__(&self, object: &XID) -> bool {
        self.to_str() < object.to_str()
    }

    fn __le__(&self, object: &XID) -> bool {
        self.to_str() <= object.to_str()
    }

    fn __gt__(&self, object: &XID) -> bool {
        self.to_str() > object.to_str()
    }

    fn __ge__(&self, object: &XID) -> bool {
        self.to_str() >= object.to_str()
    }
}
