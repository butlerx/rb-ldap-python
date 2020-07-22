"""reset-shell command"""

from bonsai import LDAPConnection

from .errors import UserNotFound


async def set_shell(
    conn: LDAPConnection, username: str, shell: str, *, commit: bool = True,
):
    """
    Reset a user's login shell

    Args:
        conn: connection to ldap server
        username: username of account to set shell
        shell: shell to set user too
        commit: flag to commit any changes

    Raises:
        UserNotFound: No user was found matching the username
    """
    results = await conn.search(
        "ou=accounts,o=redbrick",
        2,
        f"(|(uid={username})(gecos={username}))",
        attrlist=["loginShell"],
    )
    if not results:
        raise UserNotFound()
    user = results[0]
    user["loginShell"] = shell
    if commit:
        await user.modify()
