"""command to disable account"""

from bonsai import LDAPClient

from ..accounts import set_shell


async def disable(rb_client: LDAPClient, commit: bool, username: str) -> int:
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
    shell = "/usr/local/shells/disusered"
    async with rb_client.connect(is_async=True) as conn:
        await set_shell(conn, username, shell, commit=commit)
    print(f"{username} account disabled")
    return 0
