use pyo3::create_exception;
use pyo3::exceptions::PyValueError;

create_exception!(
    epyxid,
    XIDError,
    PyValueError,
    "Raised when a value cannot be parsed as an XID.\n\n\
     Subclasses :exc:`ValueError`, so ``except ValueError`` also catches it."
);
