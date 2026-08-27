"""
epyxid - A Python wrapper around Rust implementation of XID (Globally Unique ID Generator).

Author: Aleksandr Shpak
Email: shpaker@gmail.com
License: MIT
URL: https://github.com/shpaker/epyxid
"""

from datetime import datetime
from typing import Final, final

__version__: Final[str]
__all__ = [
    "__version__",
    "XIDError",
    "XID",
    "xid_create",
    "xid_from_str",
    "xid_from_bytes",
]


class XIDError(ValueError):
    """
    Exception raised when XID operations fail.

    This error is raised when attempting to create an XID from invalid
    string or bytes data, or when other XID operations encounter errors.

    Subclasses ValueError, so ``except ValueError`` also catches it.
    """


@final
class XID:
    """
    Globally unique, sortable ID generator.

    XID is a fast, globally unique, and sortable ID generator. Each ID
    consists of:
    - 4-byte timestamp (Unix time in seconds)
    - 3-byte machine ID
    - 2-byte process ID
    - 3-byte counter

    Ordering is the lexicographic order of the raw bytes, so IDs sort by
    creation time with one-second granularity. Within the same second the
    machine and process bytes decide the order, not the actual creation
    order, so IDs from different processes are not ordered by creation
    time below that resolution.

    Note:
        The embedded timestamp is a 32-bit value and wraps in 2106.

    Example:
        >>> xid = XID()
        >>> len(str(xid))
        20
        >>> XID("9m4e2mr0ui3e8a215n4g").as_bytes()
        b'M\\x88\\xe1[`\\xf4\\x86\\xe4(A-\\xc9'
    """

    def __new__(cls, value: str | bytes | None = None) -> "XID":
        """
        Create a new XID instance.

        Args:
            value: Optional string or bytes representation of an existing XID.
                  If None, generates a new unique XID. Only str and bytes are
                  accepted; other sequences raise TypeError.

        Returns:
            A new XID instance.

        Raises:
            TypeError: If the value is neither str, bytes, nor None.
            XIDError: If the provided value is not a valid XID representation.

        Example:
            >>> xid1 = XID()  # Generate new ID
            >>> xid2 = XID("9m4e2mr0ui3e8a215n4g")  # From string
            >>> xid3 = XID(b'M\\x88\\xe1[`\\xf4\\x86\\xe4(A-\\xc9')  # From bytes
            >>> xid2 == xid3
            True
        """

    def as_bytes(self) -> bytes:
        """
        Return the binary (12-byte) representation of the XID.

        Returns:
            A bytes object containing the 12-byte binary representation
            of the XID.

        Example:
            >>> xid = XID()
            >>> binary = xid.as_bytes()
            >>> len(binary)
            12
        """

    def to_str(self) -> str:
        """
        Return the string representation of the XID.

        Returns:
            A 20-character string representation of the XID.

        Example:
            >>> xid = XID()
            >>> xid_str = xid.to_str()
            >>> len(xid_str)
            20
        """

    @property
    def machine(self) -> bytes:
        """
        Extract the 3-byte machine identifier from the XID.

        Returns:
            A bytes object containing the 3-byte machine ID.

        Example:
            >>> xid = XID()
            >>> machine_id = xid.machine
            >>> len(machine_id)
            3
        """

    @property
    def pid(self) -> int:
        """
        Extract the 2-byte process ID from the XID.

        This is the OS process id truncated to 16 bits. Inside Linux
        containers it is additionally XOR-ed with a hash of
        ``/proc/self/cpuset``, so it does not necessarily equal
        ``os.getpid()``.

        Returns:
            An integer representing the process ID (0-65535).

        Example:
            >>> xid = XID()
            >>> process_id = xid.pid
        """

    @property
    def time(self) -> datetime:
        """
        Extract the timestamp from the XID.

        Returns:
            A datetime of when the XID was created.

        Example:
            >>> xid = XID()
            >>> creation_time = xid.time
        """

    @property
    def counter(self) -> int:
        """
        Extract the 3-byte counter value from the XID.

        Returns:
            An integer representing the incrementing counter (0-16777215).

        Example:
            >>> xid = XID()
            >>> counter_value = xid.counter
        """

    def __hash__(self) -> int:
        """
        Return the hash value of the XID.

        The hash is derived from the raw bytes through Python, so it follows
        PYTHONHASHSEED randomization and differs between processes.

        Returns:
            An integer hash value suitable for use in sets and dictionaries.
        """

    def __bytes__(self) -> bytes:
        """
        Return the binary representation of the XID.

        Equivalent to as_bytes().

        Returns:
            A bytes object containing the 12-byte binary representation.
        """

    def __str__(self) -> str:
        """
        Return the string representation of the XID.

        Equivalent to to_str().

        Returns:
            A 20-character string representation.
        """

    def __repr__(self) -> str:
        """
        Return the official string representation of the XID.

        Returns:
            A string in the format '<XID: xxxxx...>' containing the XID value.
        """

    def __eq__(self, other: object, /) -> bool:
        """Return True if self == other. Non-XID operands compare unequal."""

    def __ne__(self, other: object, /) -> bool:
        """Return True if self != other. Non-XID operands compare unequal."""

    def __lt__(self, other: "XID", /) -> bool:
        """Return True if self < other (raw byte order)."""

    def __le__(self, other: "XID", /) -> bool:
        """Return True if self <= other (raw byte order)."""

    def __gt__(self, other: "XID", /) -> bool:
        """Return True if self > other (raw byte order)."""

    def __ge__(self, other: "XID", /) -> bool:
        """Return True if self >= other (raw byte order)."""


def xid_create() -> XID:
    """
    Generate a new globally unique XID.

    Creates a new XID with the current timestamp, machine ID, process ID,
    and an incrementing counter.

    Returns:
        A new XID instance.

    Raises:
        XIDError: If the system clock is set before the Unix epoch.

    Example:
        >>> xid = xid_create()
        >>> len(str(xid))
        20
    """


def xid_from_str(s: str) -> XID:
    """
    Create an XID from its string representation.

    Args:
        s: A 20-character string representing an XID.

    Returns:
        An XID instance created from the string.

    Raises:
        XIDError: If the string is not a valid XID representation.

    Example:
        >>> xid = xid_from_str("9m4e2mr0ui3e8a215n4g")
    """


def xid_from_bytes(b: bytes) -> XID:
    """
    Create an XID from its binary representation.

    Args:
        b: A 12-byte bytes object representing an XID.

    Returns:
        An XID instance created from the bytes.

    Raises:
        XIDError: If the bytes do not represent a valid XID.

    Example:
        >>> xid = xid_from_bytes(b'M\\x88\\xe1[`\\xf4\\x86\\xe4(A-\\xc9')
    """
