"""command for adding user"""

from os import getuid
from pwd import getpwuid

from bonsai import LDAPClient
from mailmanclient import Client

from ..accounts import (
    check_username_free,
    create_account,
    find_available_uid,
    search_dcu,
)
from ..accounts.errors import DuplicateUser, UnknownID
from ..accounts.types import RBUser
from ..mail import RBMail


async def add(
    rb_client: LDAPClient,
    dcu_client: LDAPClient,
    smtp_client: RBMail,
    mailman: Client,
    commit: bool,
    username: str,
    *,
    id: str,
) -> int:
    """
    Add user to ldap

    Args:
        rb_client: ldap client configured for redbrick ldap
        dcu_client: ldap client configured for dcu AD
        smtp_client: redbrick smtp client
        mailman: mailman rest client
        commit: flag to commit any changes
        username: username of user to be created
        id: dcu student id

    Returns:
        Returns int to indicate exit code

    Raises:
        DuplicateUser: Thrown if the supplied username already exists
        UnkownID: Thrown is the supplied student id does not return an users
    """
    async with rb_client.connect(is_async=True) as conn:
        if not await check_username_free(conn, username):
            raise DuplicateUser()
        async with dcu_client.connect(is_aysnc=True) as dcu_conn:
            students = await search_dcu(dcu_conn, dcu_id=id)
            if not students:
                raise UnknownID()
        uid = await find_available_uid(conn)
        new_user = RBUser.from_dcu(
            students[0],
            username,
            uid=uid,
            created_by=getpwuid(getuid())[
                0
            ],  # TODO: this will return root given we dont have local account any more
            hosts=["azazel", "pygmalion"],  # TODO: Make hosts configurable
        )
        if commit:
            await create_account(conn, smtp_client, mailman, new_user)
    print(new_user)
    return 0
