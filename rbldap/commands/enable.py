"""enable command"""

from ldap3 import MODIFY_REPLACE

from ..accounts.clients import LDAPConnection


async def enable(rb_client: LDAPConnection, commit: bool, username: str) -> int:
    """
    Renable a Users LDAP Account

    Args:
        rb_client: ldap client configured for redbrick ldap
        commit: flag to commit any changes
        username: username of account to reset

    Returns:
        Returns int to indicate exit code

    Raises:
        UserNotFound: No user was found matching the username
    """
    async with rb_client.connect() as conn:
        if commit:
            await conn.modify(
                f"uid={username},ou=accounts,o=redbrick",
                {"loginShell": [(MODIFY_REPLACE, ["/usr/local/shells/shell"])]},
            )
    print(f"{username} Account re-enabled")
    return 0
