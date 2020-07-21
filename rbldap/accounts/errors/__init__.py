"""account excpetion"""

from .duplicate import DuplicateUser
from .id import UnknownID

__all__ = ["UnknownID", "DuplicateUser"]
