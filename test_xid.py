from typing import Union, Optional

from epyxid import xid_from_bytes, xid_create, XID, XIDError, xid_from_str

from pytest import raises, param, mark

XID_STR = '9m4e2mr0ui3e8a215n4g'
XID_BYTES = bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d, 0xc9])


def test_create_func() -> None:
    xid = xid_create()
    assert xid is not None


def test_create_cls() -> None:
    xid = XID()
    assert xid is not None


@mark.parametrize(
    ('value',),
    [
        param(None),
        param(XID_BYTES),
        param(XID_STR),
    ],
)
def test_create_cls_param(value: Optional[Union[str, bytes]], ) -> None:
    xid = XID(value)
    assert xid is not None


def test_create_cls_type_error() -> None:
    with raises(TypeError):
        xid = XID(42)


def test_create_cls_xid_error() -> None:
    with raises(XIDError):
        xid = XID('42')


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


def test_hash() -> None:
    xid = xid_from_bytes(XID_BYTES)
    assert isinstance(hash(xid), int)


def test_from_bytes_invalid_length() -> None:
    with raises(ValueError):
        xid_from_bytes(bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d]))
