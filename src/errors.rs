use pyo3::create_exception;
use pyo3::exceptions::PyValueError;

create_exception!(mymodule, XIDError, PyValueError);
