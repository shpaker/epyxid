use crate::utils::{xid_create, xid_from_bytes, xid_from_str};
use std::hash::{DefaultHasher, Hash, Hasher};

use pyo3::types::PyAny;
use pyo3::types::{PyBytes, PyDateTime};
use pyo3::{pyclass, pymethods, Bound, FromPyObject, PyResult, Python};
use xid::Id;

#[derive(FromPyObject)]
enum XIDReprTypes {
    #[pyo3(transparent, annotation = "str")]
    String(String),
    #[pyo3(transparent, annotation = "bytes")]
    Bytes(Vec<u8>),
}

#[pyclass]
#[allow(clippy::upper_case_acronyms)]
pub struct XID(pub Id);

#[pymethods]
impl XID {
    #[new]
    #[pyo3(signature = (data=None))]
    fn py_new(data: Option<XIDReprTypes>) -> PyResult<XID> {
        match data {
            None => xid_create(),
            Some(repr_value) => match repr_value {
                XIDReprTypes::String(value) => xid_from_str(value.as_str()),
                XIDReprTypes::Bytes(value) => xid_from_bytes(value),
            },
        }
    }

    fn as_bytes<'p>(&self, _py: Python<'p>) -> Bound<'p, PyBytes> {
        PyBytes::new(_py, self.0.as_bytes())
    }

    fn to_str(&self) -> String {
        self.0.to_string()
    }

    #[getter]
    fn machine<'p>(&self, _py: Python<'p>) -> Bound<'p, PyBytes> {
        PyBytes::new(_py, &self.0.machine())
    }

    #[getter]
    fn pid(&self) -> u16 {
        self.0.pid()
    }

    #[getter]
    fn time<'p>(&self, _py: Python<'p>) -> PyResult<Bound<'p, PyDateTime>> {
        let raw = self.0.as_bytes();
        let unix_ts = u32::from_be_bytes([raw[0], raw[1], raw[2], raw[3]]);
        PyDateTime::from_timestamp(_py, unix_ts as f64, None)
    }

    #[getter]
    fn counter(&self) -> u32 {
        self.0.counter()
    }

    fn __bytes__<'p>(&self, _py: Python<'p>) -> Bound<'p, PyBytes> {
        self.as_bytes(_py)
    }

    fn __str__(&self) -> String {
        self.to_str()
    }

    fn __repr__(&self) -> String {
        format!("<XID: {}>", self.to_str())
    }

    fn __eq__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        match other.cast::<XID>() {
            Ok(xid) => {
                let borrowed = xid.borrow();
                Ok(self.0.as_bytes() == borrowed.0.as_bytes())
            }
            Err(_) => Ok(false),
        }
    }

    fn __ne__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        match other.cast::<XID>() {
            Ok(xid) => {
                let borrowed = xid.borrow();
                Ok(self.0.as_bytes() != borrowed.0.as_bytes())
            }
            Err(_) => Ok(true),
        }
    }

    fn __lt__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        match other.cast::<XID>() {
            Ok(xid) => {
                let borrowed = xid.borrow();
                Ok(self.0.as_bytes() < borrowed.0.as_bytes())
            }
            Err(_) => Err(pyo3::exceptions::PyTypeError::new_err(
                "'<' not supported between instances of 'XID' and other types",
            )),
        }
    }

    fn __le__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        match other.cast::<XID>() {
            Ok(xid) => {
                let borrowed = xid.borrow();
                Ok(self.0.as_bytes() <= borrowed.0.as_bytes())
            }
            Err(_) => Err(pyo3::exceptions::PyTypeError::new_err(
                "'<=' not supported between instances of 'XID' and other types",
            )),
        }
    }

    fn __gt__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        match other.cast::<XID>() {
            Ok(xid) => {
                let borrowed = xid.borrow();
                Ok(self.0.as_bytes() > borrowed.0.as_bytes())
            }
            Err(_) => Err(pyo3::exceptions::PyTypeError::new_err(
                "'>' not supported between instances of 'XID' and other types",
            )),
        }
    }

    fn __ge__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        match other.cast::<XID>() {
            Ok(xid) => {
                let borrowed = xid.borrow();
                Ok(self.0.as_bytes() >= borrowed.0.as_bytes())
            }
            Err(_) => Err(pyo3::exceptions::PyTypeError::new_err(
                "'>=' not supported between instances of 'XID' and other types",
            )),
        }
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.0.hash(&mut hasher);
        hasher.finish()
    }
}
