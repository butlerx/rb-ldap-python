"""reset command"""

from bonsai import LDAPClient, LDAPEntry, LDAPModOp

from ...accounts import generate_passwd
from ...accounts.errors import UserNotFound
from ...mail import RBMail


async def reset_password(
    rb_client: LDAPClient, smtp_client: RBMail, commit: bool, username: str,
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
    async with rb_client.connect(is_async=True) as conn:
        results = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            f"((uid={username})|(gecos={username}))",
            attrlist=["altmail"],
        )
        if not results:
            raise UserNotFound()
        user = results[0]
        password = generate_passwd(12)
        user.change_attribute("userPassword", LDAPModOp.REPLACE, password)
        user.modify()
    async with smtp_client:
        await smtp_client.send_password_reset(user["altmail"], username, password)
    return 0
