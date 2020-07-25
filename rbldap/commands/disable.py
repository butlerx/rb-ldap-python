"""command to disable account"""

from ldap3 import MODIFY_REPLACE

from ..accounts.clients import LDAPConnection


async def disable(rb_client: LDAPConnection, commit: bool, username: str) -> int:
    """
    Disable a Users LDAP Account

    Args:
        rb_client: ldap client configured for redbrick ldap
        commit: flag to commit any changes
        username: username of user to disable

    Returns:
        Returns int to indicate exit code

    Raises:
        UserNotFound: raised if the user is not found
    """
    async with rb_client.connect() as conn:
        if commit:
            await conn.modify(
                f"uid={username},ou=accounts,o=redbrick",
                {"loginShell": [(MODIFY_REPLACE, ["/usr/local/shells/disusered"])]},
            )
    print(f"{username} account disabled")
    return 0
