"""unpaid users alerting"""

from asyncio import gather

from ...accounts.clients import LDAPConnection
from ...mail import RBMail


async def alert_unpaid(rb_client: LDAPConnection, smtp_client: RBMail) -> int:
    """
    Send email to all users with unpaid account altmails telling them their account is unpaid

    Args:
        rb_client: ldap client configured for redbrick ldap
        smtp: smtp client for contacting email

    Returns:
        int indicating the exit code
    """

    async with rb_client.connect() as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(&(|(yearspaid=-1)(yearspaid=0))(|(usertype=member)(usertype=associate)(usertype=staff))",
            attributes=["uid", "yearsPaid", "cn", "altmail", "id"],
        )
    users = [user for user in res if user["attributes"]["yearsPaid"][0] in [-1, 0]]

    async with smtp_client:
        await gather(
            *[
                smtp_client.send_unpaid_alert(
                    user["attributes"]["uid"][0],
                    user["attributes"]["yearsPaid"][0],
                    user["attributes"]["altmail"][0],
                    user["attributes"]["cn"][0],
                    user["attributes"]["id"][0],
                )
                for user in users
            ]
        )

    print(f"{len(users)} accounts disabled")

    return 0
