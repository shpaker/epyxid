//! Python bindings for the [`xid`] crate: fast, globally unique,
//! lexicographically sortable identifiers.

use pyo3::prelude::{
    pymodule, wrap_pyfunction, Bound, PyModule, PyModuleMethods, PyResult, Python,
};

use crate::errors::XIDError;
use crate::utils::{xid_create, xid_from_bytes, xid_from_str};
use crate::wrapper::XID;

mod errors;
mod utils;
mod wrapper;

#[pymodule]
fn epyxid(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<XID>()?;
    m.add_function(wrap_pyfunction!(xid_create, m)?)?;
    m.add_function(wrap_pyfunction!(xid_from_str, m)?)?;
    m.add_function(wrap_pyfunction!(xid_from_bytes, m)?)?;
    m.add("XIDError", py.get_type::<XIDError>())?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
