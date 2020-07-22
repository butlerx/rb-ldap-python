"""new year automation"""

from asyncio import gather

from bonsai import LDAPClient
from mailmanclient import Client

from ...accounts import decrement_user, del_user, set_shell


async def new_year(
    rb_client: LDAPClient,
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

    async with rb_client.connect(is_async=True) as conn:
        all_users = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(|(usertype=member)(usertype=associate)(usertype=staff)",
            attrlist=["uid", "yearsPaid", "homeDirectory", "usertype"],
        )
        years_0_or_more = [user for user in all_users if user["yearsPaid"][0] >= 0]
        years_0 = [user for user in all_users if user["yearsPaid"][0] == 0]
        years_minus_1 = [user for user in all_users if user["yearsPaid"][0] == -1]

        # Disable all accounts that havent paid in a year
        await gather(
            *[
                set_shell(
                    conn,
                    user["uid"][0],
                    shell="/usr/local/shells/expired",
                    commit=commit,
                )
                for user in years_0
            ]
        )
        # Delete all accounts that havent paid in 2 year
        await gather(
            *[del_user(user, mailman=mailman, commit=commit) for user in years_minus_1]
        )
        await gather(*[decrement_user(user, commit=commit) for user in years_0_or_more])

    print(f"{len(years_0)} accounts disabled")
    print(f"{len(years_minus_1)} accounts deleted")
    return 0
