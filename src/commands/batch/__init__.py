"""
Batch Automation commands
These commands are rarely idompotent.
"""
from .alert_unpaid import alert_unpaid_users_cli
from .delete_unpaid import delete_unpaid_users_cli
from .disable_unpaid import disable_unpaid_users_cli
from .new_year import new_year_cli

__all__ = [
    "alert_unpaid_users_cli",
    "delete_unpaid_users_cli",
    "disable_unpaid_users_cli",
    "new_year_cli",
]
