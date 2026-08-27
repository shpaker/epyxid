use pyo3::create_exception;
use pyo3::exceptions::PyValueError;
use pyo3::PyErr;
use xid::ParseIdError;

create_exception!(
    epyxid,
    XIDError,
    PyValueError,
    "Raised when a value cannot be parsed as an XID.\n\n\
     Subclasses :exc:`ValueError`, so ``except ValueError`` also catches it."
);

/// Longest input echoed back in an error message.
const MAX_ECHO: usize = 64;

/// Render untrusted input for an error message with control characters escaped,
/// truncating anything unreasonably long.
fn echo(input: &str) -> String {
    match input.char_indices().nth(MAX_ECHO) {
        Some((cut, _)) => format!("{:?}...", &input[..cut]),
        None => format!("{input:?}"),
    }
}

/// Build the error raised when a string cannot be parsed as an XID.
pub(crate) fn str_parse_err(error: &ParseIdError, input: &str) -> PyErr {
    let detail = match error {
        ParseIdError::InvalidLength(len) => {
            format!("expected 20 characters, got {len}")
        }
        ParseIdError::InvalidCharacter(_) => "expected characters from [0-9a-v] only".to_owned(),
    };
    XIDError::new_err(format!("invalid XID string {}: {detail}", echo(input)))
}

/// Build the error raised when a byte string cannot be parsed as an XID.
pub(crate) fn bytes_parse_err(len: usize) -> PyErr {
    XIDError::new_err(format!(
        "invalid XID bytes: expected exactly 12 bytes, got {len}"
    ))
}
