"""delete user account"""
from shutil import rmtree

from mailmanclient import Client

from .clients import LDAPConnection


async def del_user(conn: LDAPConnection, user: dict, mailman: Client) -> None:
    """
    Delete an user, all their files and unsubscribe them from announces

    Args:
        conn: connection to ldap server
        user: ldap entry for given user
        mailman: mailman Rest Client
    """
    await conn.delete(user["dn"])
    uid = user["attributes"]["uid"][0]
    rmtree(user["attributes"]["homeDirectory"][0])
    rmtree(f"/webtree/{uid[:1]}/{uid}")
    mailing_list = mailman.get_list("announce-redbrick")
    mailing_list.unsubscribe(f"{uid}@redbrick.dcu.ie")
