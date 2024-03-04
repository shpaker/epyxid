mod xid_wrapper;

use std::str::FromStr;

use pyo3::exceptions::PyException;
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};
use crate::xid_wrapper::XID;
pyo3::create_exception!(mymodule, XIDError, PyException);

#[pymodule]
fn epyxid(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<XID>()?;
    m.add("XIDError", _py.get_type::<XIDError>())?;
    Ok(())
}
