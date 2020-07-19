"""search rb & dcu ldap"""

from .dcu import search_dcu
from .redbrick import search_rb

__all__ = ["search_dcu", "search_rb"]
