from datetime import datetime
from typing import Optional, Union

__version__: str


class XIDError(ValueError):
    pass


class XID:
    """
    Globally unique sortable id.
    """

    def __new__(cls, value: Optional[Union[str, bytes]] = None):
        pass

    def as_bytes(self) -> bytes:
        """
        The binary representation of the id.
        """

    def to_str(self) -> str:
        """
        The string representation of the id.
        """

    @property
    def machine(self) -> bytes:
        """
        Extract the 3-byte machine id.
        """

    @property
    def pid(self) -> int:
        """
        Extract the process id.
        """

    @property
    def time(self) -> datetime:
        """
        Extract the timestamp.
        """

    @property
    def counter(self) -> int:
        """
        Extract the incrementing counter.
        """

    def __hash__(self) -> int: ...

    def __bytes__(self) -> bytes: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, object: 'XID') -> bool: ...

    def __ne__(self, object: 'XID') -> bool: ...

    def __lt__(self, object: 'XID') -> bool: ...

    def __le__(self, object: 'XID') -> bool: ...

    def __gt__(self, object: 'XID') -> bool: ...

    def __ge__(self, object: 'XID') -> bool: ...


def xid_create() -> XID:
    """
    Generate a new globally unique id.
    """


def xid_from_str(s: str) -> XID:
    """
    Create an id from its string representation.
    """


def xid_from_bytes(b: bytes) -> XID:
    """
    Create an id from bytes.
    """
