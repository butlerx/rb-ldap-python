"""new year automation"""

from asyncio import gather

from mailmanclient import Client

from ldap3 import MODIFY_INCREMENT, MODIFY_REPLACE

from ...accounts import del_user
from ...accounts.clients import LDAPConnection


async def new_year(
    rb_client: LDAPConnection,
    mailman: Client,
    commit: bool,
    *,
    i_know_what_im_doing: bool = False,
) -> int:
    """
    To Be run at the beginning of each year prior to C&S

    Preform yearly update:
      - Set newbie to false
      - Decrement Years Paid of all users by 1
      - Disable all accounts with years paid at 0.
      - Delete all accounts with years paid of -1

    Args:
        rb_client: ldap client configured for redbrick ldap
        mailman: mailman Rest Client
        commit: flag to commit any changes
        i_know_what_im_doing: Flag to indicate to skip prompt

    Returns:
        int indicating the exit code

    """

    if not i_know_what_im_doing and not bool(
        input(
            "Perform yearly update this is not idempont and needs to only be run once [y/N]: "
        )
        in ["y", "Y", "yes"]
    ):
        return 1

    async with rb_client.connect() as conn:
        all_users = await conn.search(
            "ou=accounts,o=redbrick",
            "(|(usertype=member)(usertype=associate)(usertype=staff)",
            attributes=["uid", "yearsPaid", "homeDirectory", "usertype"],
        )
        years_0 = [
            user for user in all_users if user["attributes"]["yearsPaid"][0] == 0
        ]
        years_minus_1 = [
            user for user in all_users if user["attributes"]["yearsPaid"][0] == -1
        ]

        if commit:
            # Disable all accounts that havent paid in a year
            await gather(
                *[
                    conn.modify(
                        user["dn"],
                        {
                            "loginShell": [
                                (MODIFY_REPLACE, ["/usr/local/shells/expired"])
                            ],
                            "newbie": [(MODIFY_REPLACE, [False])],
                            "yearsPaid": [(MODIFY_INCREMENT, [-1])],
                        },
                    )
                    for user in years_0
                ]
            )
            # Delete all accounts that havent paid in 2 year
            await gather(
                *[del_user(conn, user, mailman=mailman) for user in years_minus_1]
            )
            await gather(
                *[
                    conn.modify(
                        user["dn"],
                        {
                            "newbie": [(MODIFY_REPLACE, [False])],
                            "yearsPaid": [(MODIFY_INCREMENT, [-1])],
                        },
                    )
                    for user in all_users
                    if user["attributes"]["yearsPaid"][0] > 0
                ]
            )

    print(f"{len(years_0)} accounts disabled")
    print(f"{len(years_minus_1)} accounts deleted")
    return 0
