"""unpaid users alerting"""

from asyncio import gather

from bonsai import LDAPClient

from ...mail import RBMail


async def alert_unpaid(rb_client: LDAPClient, smtp_client: RBMail) -> int:
    """
    Send email to all users with unpaid account altmails telling them their account is unpaid

    Args:
        rb_client: ldap client configured for redbrick ldap
        smtp: smtp client for contacting email

    Returns:
        int indicating the exit code
    """

    async with rb_client.connect(is_async=True) as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(&(|(yearspaid=-1)(yearspaid=0))(|(usertype=member)(usertype=associate)(usertype=staff))",
            attrlist=["uid", "yearsPaid", "cn", "altmail", "id"],
        )
    async with smtp_client:
        await gather(
            *[
                smtp_client.send_unpaid_alert(
                    user["uid"][0],
                    user["yearsPaid"][0],
                    user["altmail"][0],
                    user["cn"][0],
                    user["id"][0],
                )
                for user in res
                if user["yearsPaid"][0] != -1 or user["yearsPaid"][0] != 0
            ]
        )

    return 0
