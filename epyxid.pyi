"""
epyxid - A Python wrapper around Rust implementation of XID (Globally Unique ID Generator).

Author: Aleksandr Shpak
Email: shpaker@gmail.com
License: MIT
URL: https://github.com/shpaker/epyxid
"""

from datetime import datetime
from typing import Optional, Union

__version__: str
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
    """


class XID:
    """
    Globally unique, sortable ID generator.

    XID is a fast, globally unique, and sortable ID generator. Each ID
    consists of:
    - 4-byte timestamp (Unix time in seconds)
    - 3-byte machine ID
    - 2-byte process ID
    - 3-byte counter

    IDs are sortable by their creation time and are globally unique across
    different machines and processes.

    Example:
        >>> xid = XID()
        >>> print(xid)
        'cu701mcr9ij74n2hajpg'
        >>> print(xid.time)
        2024-12-31 23:59:59
    """

    def __new__(cls, value: Optional[Union[str, bytes]] = None) -> "XID":
        """
        Create a new XID instance.

        Args:
            value: Optional string or bytes representation of an existing XID.
                  If None, generates a new unique XID.

        Returns:
            A new XID instance.

        Raises:
            XIDError: If the provided value is not a valid XID representation.

        Example:
            >>> xid1 = XID()  # Generate new ID
            >>> xid2 = XID("cu701mcr9ij74n2hajpg")  # From string
            >>> xid3 = XID(b'...')  # From bytes
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
            A datetime object representing when the XID was created.

        Example:
            >>> xid = XID()
            >>> creation_time = xid.time
            >>> print(creation_time)
            2024-12-31 23:59:59
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

    def __eq__(self, object: 'XID') -> bool:
        """Return True if self == object."""

    def __ne__(self, object: 'XID') -> bool:
        """Return True if self != object."""

    def __lt__(self, object: 'XID') -> bool:
        """Return True if self < object (sorted by creation time)."""

    def __le__(self, object: 'XID') -> bool:
        """Return True if self <= object (sorted by creation time)."""

    def __gt__(self, object: 'XID') -> bool:
        """Return True if self > object (sorted by creation time)."""

    def __ge__(self, object: 'XID') -> bool:
        """Return True if self >= object (sorted by creation time)."""


def xid_create() -> XID:
    """
    Generate a new globally unique XID.

    Creates a new XID with the current timestamp, machine ID, process ID,
    and an incrementing counter.

    Returns:
        A new XID instance.

    Example:
        >>> xid = xid_create()
        >>> print(xid)
        'cu701mcr9ij74n2hajpg'
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
        >>> xid = xid_from_str("cu701mcr9ij74n2hajpg")
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
        >>> xid = xid_from_bytes(b'...')
    """
