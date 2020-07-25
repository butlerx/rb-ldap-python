"""reset command"""

from ldap3 import MODIFY_REPLACE

from ...accounts import generate_passwd
from ...accounts.clients import LDAPConnection
from ...accounts.errors import UserNotFound
from ...mail import RBMail


async def reset_password(
    rb_client: LDAPConnection, smtp_client: RBMail, commit: bool, username: str,
) -> int:
    """
    Reset a users password

    Args:
        rb_client: ldap client configured for redbrick ldap
        smtp_client: redbrick smtp client
        commit: flag to commit any changes
        username: username of account to reset

    Returns:
        Returns int to indicate exit code

    Raises:
        UserNotFound: No user was found matching the username
    """
    async with rb_client.connect() as conn:
        password = generate_passwd(12)
        if commit:
            await conn.modify(
                f"uid={username},ou=accounts,o=redbrick",
                {"userPassword": [(MODIFY_REPLACE, [password])]},
            )
            results = await conn.search(
                "ou=accounts,o=redbrick",
                f"(|(uid={username})(gecos={username}))",
                attributes=["altmail"],
            )
            async with smtp_client:
                await smtp_client.send_password_reset(
                    results[0]["attributes"]["altmail"][0], username, password
                )
    print(f"{username} password has been reset")
    return 0
