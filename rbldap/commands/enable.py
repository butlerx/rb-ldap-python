"""enable command"""

from bonsai import LDAPClient

from ..accounts import set_shell


async def enable(rb_client: LDAPClient, commit: bool, username: str) -> int:
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
    async with rb_client.connect(is_async=True) as conn:
        await set_shell(conn, username, shell="/usr/local/shells/shell", commit=commit)
    print(f"{username} Account re-enabled")
    return 0
