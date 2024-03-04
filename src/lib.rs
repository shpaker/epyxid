use std::str::FromStr;

use pyo3::prelude::{pymodule, PyModule, PyResult, Python};
use pyo3::wrap_pyfunction;

use crate::errors::XIDError;
use crate::utils::{xid_create, xid_from_bytes, xid_from_str};
use crate::wrapper::XID;

mod errors;
mod utils;
mod wrapper;

#[pymodule]
fn epyxid(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<XID>()?;
    m.add_function(wrap_pyfunction!(xid_create, m)?)?;
    m.add_function(wrap_pyfunction!(xid_from_str, m)?)?;
    m.add_function(wrap_pyfunction!(xid_from_bytes, m)?)?;
    m.add("XIDError", _py.get_type::<XIDError>())?;
    Ok(())
}
