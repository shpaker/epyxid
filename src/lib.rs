extern crate core;

use pyo3::prelude::{
    pymodule, wrap_pyfunction, Bound, PyModule, PyModuleMethods, PyResult, Python,
};

use crate::errors::XIDError;
use crate::utils::{xid_create, xid_from_bytes, xid_from_str};
use crate::wrapper::XID;

const PY_MODULE_VERSION: &str = "0.3.2";

mod errors;
mod utils;
mod wrapper;

#[pymodule]
fn epyxid(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<XID>()?;
    m.add_function(wrap_pyfunction!(xid_create, m)?)?;
    m.add_function(wrap_pyfunction!(xid_from_str, m)?)?;
    m.add_function(wrap_pyfunction!(xid_from_bytes, m)?)?;
    m.add("XIDError", py.get_type_bound::<XIDError>())?;
    m.add("__version__", PY_MODULE_VERSION)?;
    Ok(())
}
