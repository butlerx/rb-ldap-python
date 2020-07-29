"""disable unpaid automation"""

from asyncio import gather

from ldap3 import MODIFY_REPLACE

from ...accounts.clients import LDAPConnection


async def disable_unpaid(
    rb_client: LDAPConnection, commit: bool, *, i_know_what_im_doing: bool = False,
) -> int:
    """
    Diable all unpaid users accounts (years paid = 0)

    Args:
        rb_client: ldap client configured for redbrick ldap
        commit: flag to commit any changes
        i_know_what_im_doing: Flag to indicate to skip prompt

    Returns:
        int indicating the exit code

    """

    if not i_know_what_im_doing and not bool(
        input("Disable all unpaid users [y/N]: ") in ["y", "Y", "yes"]
    ):
        return 1

    async with rb_client.connect() as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(&(yearspaid=0)(|(usertype=member)(usertype=associate)(usertype=staff))",
            attributes=["uid", "yearsPaid", "homeDirectory", "usertype"],
        )
        users = [user for user in res if user["attributes"]["yearsPaid"][0] == 0]
        if commit:
            await gather(
                *[
                    conn.modify(
                        user["dn"],
                        {
                            "loginShell": [
                                (MODIFY_REPLACE, ["/usr/local/shells/expired"])
                            ]
                        },
                    )
                    for user in users
                ]
            )

    print(f"{len(users)} accounts disabled")
    return 0
