import os
import pickle
import sys
from copy import copy, deepcopy
from datetime import datetime
from importlib.metadata import version
from threading import Lock, Thread
from subprocess import check_output

from epyxid import __version__, xid_from_bytes, xid_create, XID, XIDError, xid_from_str

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
    first, second = creator(), creator()
    assert isinstance(first, XID)
    assert len(bytes(first)) == 12
    assert len(str(first)) == 20
    assert first != second


@mark.parametrize(
    ('value',),
    [
        param(XID_BYTES),
        param(XID_STR),
    ],
)
def test_create_xid_with_params(value: str | bytes) -> None:
    parsed = XID(value)
    assert bytes(parsed) == XID_BYTES
    assert str(parsed) == XID_STR


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
    with raises(XIDError):
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
    """Each getter must expose the exact bytes embedded in the fixture ID."""
    assert XID_OBJ.machine == XID_BYTES[4:7]
    assert XID_OBJ.pid == int.from_bytes(XID_BYTES[7:9], 'big')
    assert XID_OBJ.counter == int.from_bytes(XID_BYTES[9:12], 'big')
    timestamp = int.from_bytes(XID_BYTES[:4], 'big')
    assert XID_OBJ.time == datetime.fromtimestamp(timestamp)
    assert XID_OBJ.time.tzinfo is None


@mark.parametrize(
    ('xid1_factory', 'xid2_factory', 'expected_op'),
    [
        param(lambda: XID_OBJ, lambda: XID_OBJ, lambda a, b: a == b, id='comparison_eq'),
        param(xid_create, xid_create, lambda a, b: a != b, id='comparison_ne'),
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
    """Ordering is lexicographic over all 12 bytes; the timestamp is merely the first field."""
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


def test_equality_is_symmetric_with_foreign_types() -> None:
    """Comparisons return NotImplemented for non-XID operands, so reflected ops run."""
    from unittest import mock

    assert XID_OBJ == mock.ANY
    assert mock.ANY == XID_OBJ
    assert XID_OBJ != 'not-an-xid'
    assert not XID_OBJ == 'not-an-xid'


@mark.parametrize(
    ('roundtrip',),
    [
        param(lambda x: pickle.loads(pickle.dumps(x)), id='pickle'),
        param(copy, id='copy'),
        param(deepcopy, id='deepcopy'),
    ],
)
def test_roundtrip_preserves_value(roundtrip) -> None:
    restored = roundtrip(XID_OBJ)
    assert restored == XID_OBJ
    assert bytes(restored) == XID_BYTES


def test_hash_matches_bytes_hash() -> None:
    assert hash(XID_OBJ) == hash(XID_BYTES)


def test_hash_is_randomized_per_process() -> None:
    """__hash__ delegates to Python's bytes hash, so PYTHONHASHSEED changes it."""
    code = 'from epyxid import xid_from_str; print(hash(xid_from_str("9m4e2mr0ui3e8a215n4g")))'

    def hash_with_seed(seed: str) -> str:
        env = {**os.environ, 'PYTHONHASHSEED': seed}
        return check_output([sys.executable, '-c', code], env=env, text=True).strip()

    assert hash_with_seed('1') != hash_with_seed('2')


def test_sorting_follows_byte_order() -> None:
    assert sorted([XID_LATER, XID_EARLIER]) == [XID_EARLIER, XID_LATER]
    assert (XID_LATER < XID_EARLIER) is False
    assert (XID_EARLIER < XID_LATER) is True


def test_class_is_exposed_under_package_module() -> None:
    assert XID.__module__ == 'epyxid'


def test_create_xid_accepts_value_keyword() -> None:
    assert XID(value=XID_STR) == XID_COMPARISON_1


@mark.parametrize(
    ('value',),
    [
        param(list(XID_BYTES), id='list'),
        param(tuple(XID_BYTES), id='tuple'),
        param(range(12), id='range'),
        param(bytearray(XID_BYTES), id='bytearray'),
    ],
)
def test_create_xid_rejects_non_str_bytes(value) -> None:
    """Only str and bytes are accepted; int sequences must not become IDs."""
    with raises(TypeError):
        XID(value)
    with raises(TypeError):
        xid_from_bytes(value)


def test_surrogate_string_raises_xid_error() -> None:
    """A str that is not valid UTF-8 is an invalid XID, not a type error."""
    with raises(XIDError):
        XID(b'caf\xe9'.decode('utf-8', 'surrogateescape'))


@mark.parametrize(
    ('value', 'expected_fragment'),
    [
        param('42', 'expected 20 characters, got 2', id='short_str'),
        param('9z4e2mr0ui3e8a215n4g', 'expected characters from [0-9a-v] only', id='bad_char'),
    ],
)
def test_string_error_messages_are_actionable(value: str, expected_fragment: str) -> None:
    with raises(XIDError) as info:
        XID(value)
    assert expected_fragment in str(info.value)


def test_bytes_error_message_reports_length() -> None:
    with raises(XIDError) as info:
        XID(XID_BYTES[:11])
    assert 'expected exactly 12 bytes, got 11' in str(info.value)


def test_error_message_escapes_control_characters() -> None:
    """Untrusted input is escaped so it cannot forge log lines."""
    with raises(XIDError) as info:
        XID('cnisffq7qo0qnbtbu5g\n')
    message = str(info.value)
    assert '\n' not in message
    assert '\\n' in message


def test_generated_ids_are_unique() -> None:
    """Uniqueness is the library's core guarantee, so pin it explicitly."""
    ids = {str(xid_create()) for _ in range(10_000)}
    assert len(ids) == 10_000


def test_generated_ids_are_unique_across_threads() -> None:
    results: list[list[str]] = []
    lock = Lock()

    def worker() -> None:
        batch = [str(xid_create()) for _ in range(5_000)]
        with lock:
            results.append(batch)

    threads = [Thread(target=worker) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    generated = [xid for batch in results for xid in batch]
    assert len(generated) == 40_000
    assert len(set(generated)) == 40_000


def test_generated_ids_sort_by_creation_order() -> None:
    generated = [xid_create() for _ in range(1_000)]
    assert generated == sorted(generated)


def test_version_matches_distribution_metadata() -> None:
    assert __version__ == version('epyxid')


def test_xid_error_subclasses_value_error() -> None:
    assert issubclass(XIDError, ValueError)
