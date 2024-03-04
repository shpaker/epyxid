use std::str::FromStr;

use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

use crate::xid_wrapper::{XID, XIDError};

mod xid_wrapper;

#[pymodule]
fn epyxid(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<XID>()?;
    m.add("XIDError", _py.get_type::<XIDError>())?;
    Ok(())
}
