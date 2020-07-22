"""delete user account"""
from shutil import rmtree

from bonsai import LDAPEntry
from mailmanclient import Client


async def del_user(user: LDAPEntry, mailman: Client):
    """
    Delete an user, all their files and unsubscribe them from announces

    Args:
        user: ldap entry for given user
        mailman: mailman Rest Client
    """
    await user.delete()
    uid = user["uid"][0]
    rmtree(user["homeDirectory"][0])
    rmtree(f"/webtree/{uid[:1]}/{uid}")
    mailing_list = mailman.get_list("announce-redbrick")
    mailing_list.unsubscribe(f"{uid}@redbrick.dcu.ie")
