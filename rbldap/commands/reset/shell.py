""" reset-shell command"""

from ldap3 import MODIFY_REPLACE

from ...accounts.clients import LDAPConnection


async def reset_shell(
    rb_client: LDAPConnection,
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
    async with rb_client.connect() as conn:
        if commit:
            await conn.modify(
                f"uid={username},ou=accounts,o=redbrick",
                {"loginShell": [(MODIFY_REPLACE, [shell])]},
            )
    print(f"{username} shell set to {shell}")
    return 0
