use std::time::UNIX_EPOCH;

use pyo3::exceptions::PyTypeError;
use pyo3::types::{
    PyAny, PyAnyMethods, PyBytes, PyBytesMethods, PyDateTime, PyString, PyStringMethods, PyType,
    PyTypeMethods,
};
use pyo3::{pyclass, pymethods, Bound, PyResult, Python};
use xid::Id;

use crate::errors::XIDError;
use crate::utils::{parse_bytes, parse_str, xid_create};

/// Globally unique, sortable identifier.
///
/// An XID is 12 bytes: a 4-byte big-endian Unix timestamp (seconds), a 3-byte
/// machine identifier, a 2-byte process identifier and a 3-byte counter.
///
/// Instances are immutable, hashable and totally ordered. Ordering is the
/// lexicographic order of the raw bytes, so IDs sort by creation time with
/// one-second granularity; within the same second the machine and process
/// bytes decide the order, not the actual creation order.
#[pyclass(frozen, eq, ord, module = "epyxid")]
#[derive(PartialEq, Eq, PartialOrd, Ord)]
#[allow(clippy::upper_case_acronyms)]
pub struct XID(pub Id);

#[pymethods]
impl XID {
    /// Create an XID from `str` or `bytes`, or generate a new one when omitted.
    #[new]
    #[pyo3(signature = (value=None))]
    fn py_new(value: Option<&Bound<'_, PyAny>>) -> PyResult<XID> {
        let Some(value) = value else {
            return xid_create();
        };
        if let Ok(text) = value.cast::<PyString>() {
            // `to_cow` (unlike `to_str`) is available under the limited API; it
            // fails only for strings carrying surrogates, which are never XIDs.
            let text = text
                .to_cow()
                .map_err(|_| XIDError::new_err("invalid XID string: not valid UTF-8"))?;
            return parse_str(&text).map(XID);
        }
        if let Ok(raw) = value.cast::<PyBytes>() {
            return parse_bytes(raw.as_bytes()).map(XID);
        }
        Err(PyTypeError::new_err(format!(
            "XID() argument must be str or bytes, not '{}'",
            value.get_type().name()?
        )))
    }

    /// Return the 12-byte binary representation.
    fn as_bytes<'p>(&self, py: Python<'p>) -> Bound<'p, PyBytes> {
        PyBytes::new(py, self.0.as_bytes())
    }

    /// Return the 20-character base32-hex representation.
    fn to_str(&self) -> String {
        self.0.to_string()
    }

    /// The 3-byte machine identifier embedded in the ID.
    #[getter]
    fn machine<'p>(&self, py: Python<'p>) -> Bound<'p, PyBytes> {
        PyBytes::new(py, &self.0.machine())
    }

    /// The 2-byte process identifier embedded in the ID.
    ///
    /// This is the OS process id truncated to 16 bits. Inside Linux containers
    /// the value is additionally XOR-ed with a hash of `/proc/self/cpuset`, so
    /// it does not necessarily match `os.getpid()`.
    #[getter]
    fn pid(&self) -> u16 {
        self.0.pid()
    }

    /// The creation time embedded in the ID.
    ///
    /// The returned `datetime` is **naive and expressed in the local timezone**
    /// of the machine reading it, even though the ID stores UTC seconds. Two IDs
    /// one hour apart can therefore render identically across a DST fold, and on
    /// Windows timestamps that map to a pre-1970 local time raise `OSError`.
    ///
    /// The stored timestamp is a 32-bit value and wraps in 2106.
    #[getter]
    fn time<'p>(&self, py: Python<'p>) -> PyResult<Bound<'p, PyDateTime>> {
        let unix_ts = self
            .0
            .time()
            .duration_since(UNIX_EPOCH)
            .map_err(|_| XIDError::new_err("XID timestamp is before the Unix epoch"))?
            .as_secs();
        PyDateTime::from_timestamp(py, unix_ts as f64, None)
    }

    /// The 3-byte counter embedded in the ID.
    #[getter]
    fn counter(&self) -> u32 {
        self.0.counter()
    }

    fn __bytes__<'p>(&self, py: Python<'p>) -> Bound<'p, PyBytes> {
        self.as_bytes(py)
    }

    fn __str__(&self) -> String {
        self.to_str()
    }

    fn __repr__(&self) -> String {
        format!("<XID: {}>", self.0)
    }

    /// Hash the raw bytes through Python so the value follows `PYTHONHASHSEED`
    /// randomization instead of being constant across processes.
    fn __hash__(&self, py: Python<'_>) -> PyResult<isize> {
        PyBytes::new(py, self.0.as_bytes()).hash()
    }

    fn __reduce__<'p>(&self, py: Python<'p>) -> (Bound<'p, PyType>, (String,)) {
        (py.get_type::<XID>(), (self.to_str(),))
    }
}
