"""delete user account"""
from bonsai import LDAPEntry


async def decrement_user(user: LDAPEntry, *, commit: bool = True):
    """
    Decrement user year paid by 1 and ensure newbie is false

    Args:
        user: ldap entry for given user
        commit: flag to commit any changes
    """
    user["newbie"] = False
    user["yearsPaid"] -= 1
    if not commit:
        return
    await user.modify()
