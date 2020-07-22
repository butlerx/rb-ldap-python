"""disable unpaid automation"""

from asyncio import gather

from bonsai import LDAPClient

from ...accounts import set_shell


async def disable_unpaid(
    rb_client: LDAPClient, commit: bool, *, verify_disable: bool = False
) -> int:
    """
    Diable all unpaid users accounts (years paid = 0)

    Args:
        rb_client: ldap client configured for redbrick ldap
        commit: flag to commit any changes
        verify_disable: Flag to indicate to skip prompt

    Returns:
        int indicating the exit code

    """

    if not verify_disable and not bool(
        input("Disable all unpaid users [y/N]: ") in ["y", "Y", "yes"]
    ):
        return 1

    async with rb_client.connect(is_async=True) as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(&((yearspaid=0))(|(usertype=member)(usertype=associate)(usertype=staff))",
            attrlist=["uid", "yearsPaid", "homeDirectory", "usertype"],
        )
        users = [user for user in res if user["yearsPaid"][0] == 0]
        await gather(
            *[
                set_shell(
                    conn,
                    user["uid"][0],
                    shell="/usr/local/shells/expired",
                    commit=commit,
                )
                for user in users
            ]
        )

    print(f"{len(users)} accounts disabled")
    return 0
