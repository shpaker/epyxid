from epyxid import xid_from_bytes, xid_from_str, xid_create
from pytest import raises

XID_STR = '9m4e2mr0ui3e8a215n4g'
XID_BYTES = bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d, 0xc9])


def test_create() -> None:
    xid = xid_create()
    assert xid is not None


def test_from_str_valid() -> None:
    xid = xid_from_str(XID_STR)
    assert bytes(xid) == XID_BYTES


def test_from_str_invalid_length() -> None:
    with raises(ValueError):
        xid_from_str('9m4e2mr0ui3e8a215n4')


def test_from_str_invalid_char() -> None:
    with raises(ValueError):
        xid_from_str('9z4e2mr0ui3e8a215n4g')


def test_from_bytes_valid() -> None:
    xid = xid_from_bytes(XID_BYTES)
    assert str(xid) == XID_STR


def test_from_bytes_invalid_length() -> None:
    with raises(ValueError):
        xid_from_bytes(bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d]))
