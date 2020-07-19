"""search rb & dcu ldap"""

from .dcu import search_dcu, search_dcu_cli
from .redbrick import search_rb, search_rb_cli

__all__ = ["search_dcu", "search_rb", "search_dcu_cli", "search_rb_cli"]
