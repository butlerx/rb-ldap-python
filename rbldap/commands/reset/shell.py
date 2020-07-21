""" reset-shell command"""

from bonsai import LDAPClient

from ...accounts import set_shell


async def reset_shell(
    rb_client: LDAPClient,
    commit: bool,
    username: str,
    *,
    shell: str = "/usr/local/shells/shell",
) -> int:
    """
    Reset a user's login shell

    Args:
        rb_client: ldap client configured for redbrick ldap
        commit: flag to commit any changes
        username: username of account to reset
        shell: shell to set user too

    Returns:
        Returns int to indicate exit code

    Raises:
        UserNotFound: No user was found matching the username
    """
    async with rb_client.connect(is_async=True) as conn:
        await set_shell(conn, username, shell, commit=commit)
    print(f"{username} shell set to {shell}")
    return 0
