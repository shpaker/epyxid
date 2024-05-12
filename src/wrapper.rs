use std::hash::{DefaultHasher, Hash, Hasher};

use crate::utils::{xid_create, xid_from_bytes, xid_from_str};

use pyo3::types::{PyBytes, PyDateTime, PyString};
use pyo3::{pyclass, pymethods, Bound, FromPyObject, PyResult, Python};
use xid::Id;

#[derive(FromPyObject)]
enum XIDReprTypes<'a> {
    #[pyo3(transparent, annotation = "str")]
    String(&'a PyString),
    #[pyo3(transparent, annotation = "bytes")]
    Bytes(&'a PyBytes),
}

#[pyclass]
pub struct XID(pub Id);

#[pymethods]
impl XID {
    #[new]
    fn new<'p>(py: Python<'p>, data: Option<XIDReprTypes>) -> PyResult<XID> {
        match data {
            None => xid_create(),
            Some(repr_value) => match repr_value {
                XIDReprTypes::String(value) => xid_from_str(value.to_str().unwrap()),
                XIDReprTypes::Bytes(value) => {
                    xid_from_bytes(PyBytes::new_bound(py, value.as_bytes()))
                }
            },
        }
    }

    fn as_bytes<'p>(&self, _py: Python<'p>) -> Bound<'p, PyBytes> {
        PyBytes::new_bound(_py, self.0.as_bytes())
    }

    fn to_str(&self) -> String {
        self.0.to_string()
    }

    #[getter]
    fn machine<'p>(&self, _py: Python<'p>) -> Bound<'p, PyBytes> {
        PyBytes::new_bound(_py, &self.0.machine())
    }

    #[getter]
    fn pid(&self) -> u16 {
        self.0.pid()
    }

    #[getter]
    fn time<'p>(&self, _py: Python<'p>) -> PyResult<Bound<'p, PyDateTime>> {
        let raw = self.0.as_bytes();
        let unix_ts = u32::from_be_bytes([raw[0], raw[1], raw[2], raw[3]]);
        PyDateTime::from_timestamp_bound(_py, unix_ts as f64, None)
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

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.0.hash(&mut hasher);
        hasher.finish()
    }
}
