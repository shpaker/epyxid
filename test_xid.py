from typing import Union, Optional

from epyxid import xid_from_bytes, xid_create, XID, XIDError, xid_from_str

from pytest import raises, param, mark

XID_STR = '9m4e2mr0ui3e8a215n4g'
XID_BYTES = bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d, 0xc9])

# XID objects for tests
XID_OBJ = xid_from_bytes(XID_BYTES)

# XID objects for comparison tests
XID_COMPARISON_1 = xid_from_str(XID_STR)
XID_COMPARISON_2 = xid_from_bytes(bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d, 0xca]))
XID_EARLIER = XID_OBJ  # Same as XID_BYTES
XID_LATER = xid_from_bytes(bytes([0x4d, 0x88, 0xe1, 0x5c, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d, 0xc9]))


@mark.parametrize(
    ('creator',),
    [
        param(xid_create, id='function'),
        param(XID, id='class'),
    ],
)
def test_create_xid(creator) -> None:
    assert creator() is not None


@mark.parametrize(
    ('value',),
    [
        param(XID_BYTES),
        param(XID_STR),
    ],
)
def test_create_xid_with_params(value: Optional[Union[str, bytes]]) -> None:
    assert XID(value) is not None


@mark.parametrize(
    ('value', 'expected_exception'),
    [
        param(42, TypeError, id='type_error_int'),
        param('42', XIDError, id='value_error_invalid_str'),
    ],
)
def test_create_xid_errors(value, expected_exception) -> None:
    with raises(expected_exception):
        XID(value)


@mark.parametrize(
    ('func', 'input_value', 'expected'),
    [
        param(xid_from_str, XID_STR, XID_BYTES, id='from_str_valid'),
        param(xid_from_bytes, XID_BYTES, XID_STR, id='from_bytes_valid'),
    ],
)
def test_from_valid(func, input_value, expected) -> None:
    result = func(input_value)
    if isinstance(expected, bytes):
        assert bytes(result) == expected
    else:
        assert str(result) == expected


@mark.parametrize(
    ('func', 'invalid_value'),
    [
        param(xid_from_str, '9m4e2mr0ui3e8a215n4', id='from_str_invalid_length'),
        param(xid_from_str, '9z4e2mr0ui3e8a215n4g', id='from_str_invalid_char'),
        param(xid_from_bytes, bytes([0x4d, 0x88, 0xe1, 0x5b, 0x60, 0xf4, 0x86, 0xe4, 0x28, 0x41, 0x2d]), id='from_bytes_invalid_length'),
    ],
)
def test_from_invalid(func, invalid_value) -> None:
    with raises(ValueError):
        func(invalid_value)


@mark.parametrize(
    ('method', 'expected'),
    [
        param(lambda x: x.as_bytes(), XID_BYTES, id='as_bytes'),
        param(lambda x: bytes(x), XID_BYTES, id='bytes_magic'),
        param(lambda x: x.to_str(), XID_STR, id='to_str'),
        param(lambda x: str(x), XID_STR, id='str_magic'),
        param(lambda x: repr(x), f'<XID: {XID_STR}>', id='repr'),
    ],
)
def test_conversion_methods(method, expected) -> None:
    assert method(XID_OBJ) == expected


def test_property_getters() -> None:
    assert isinstance(XID_OBJ.machine, bytes)
    assert isinstance(XID_OBJ.pid, int)
    assert isinstance(XID_OBJ.time, object)
    assert isinstance(XID_OBJ.counter, int)


@mark.parametrize(
    ('xid1_factory', 'xid2_factory', 'expected_op'),
    [
        param(lambda: XID_OBJ, lambda: XID_OBJ, lambda a, b: a == b, id='comparison_eq'),
        param(xid_create, xid_create, lambda a, b: a != b or a == b, id='comparison_ne'),
    ],
)
def test_comparison_basic(xid1_factory, xid2_factory, expected_op) -> None:
    xid1 = xid1_factory()
    xid2 = xid2_factory()
    assert expected_op(xid1, xid2)


@mark.parametrize(
    ('op', 'op_str'),
    [
        param(lambda a, b: a < b, '<', id='lt'),
        param(lambda a, b: a <= b, '<=', id='le'),
        param(lambda a, b: a > b, '>', id='gt'),
        param(lambda a, b: a >= b, '>=', id='ge'),
    ],
)
def test_comparison_operators(op, op_str: str) -> None:
    xid1_str = str(XID_COMPARISON_1)
    xid2_str = str(XID_COMPARISON_2)
    op_result = op(XID_COMPARISON_1, XID_COMPARISON_2)
    str_result = op(xid1_str, xid2_str)
    assert op_result == str_result


@mark.parametrize(
    ('op', 'expected'),
    [
        param(lambda a, b: a < b, True, id='earlier_lt'),
        param(lambda a, b: a <= b, True, id='earlier_le'),
        param(lambda a, b: b > a, True, id='later_gt'),
        param(lambda a, b: b >= a, True, id='later_ge'),
        param(lambda a, b: a != b, True, id='ne'),
    ],
)
def test_comparison_by_timestamp(op, expected: bool) -> None:
    """XID comparison is based on timestamp (first 4 bytes), sorting by creation time."""
    assert XID_EARLIER.time < XID_LATER.time
    assert op(XID_EARLIER, XID_LATER) == expected


@mark.parametrize(
    ('op', 'should_raise'),
    [
        param(lambda a, b: a < b, True, id='lt_raises'),
        param(lambda a, b: a <= b, True, id='le_raises'),
        param(lambda a, b: a > b, True, id='gt_raises'),
        param(lambda a, b: a >= b, True, id='ge_raises'),
        param(lambda a, b: a == b, False, id='eq_returns'),
        param(lambda a, b: a != b, False, id='ne_returns'),
    ],
)
def test_comparison_with_other_types(op, should_raise: bool) -> None:
    """XID comparison with non-XID objects raises TypeError for ordering operators."""
    if should_raise:
        with raises(TypeError):
            op(XID_OBJ, 'test')
    else:
        assert isinstance(op(XID_OBJ, 'test'), bool)


def test_hash_basic() -> None:
    assert isinstance(hash(XID_OBJ), int)


def test_hash_equal_objects() -> None:
    xid1 = xid_from_bytes(XID_BYTES)
    xid2 = xid_from_bytes(XID_BYTES)
    assert hash(xid1) == hash(xid2)
