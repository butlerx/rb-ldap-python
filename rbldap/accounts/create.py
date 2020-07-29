"""user creation"""
from os import chown, makedirs, path, symlink

from mailmanclient import Client

from ..mail import RBMail
from .clients import LDAPConnection
from .types import RBUser


async def create_account(
    conn: LDAPConnection, smtp: RBMail, mailman: Client, new_user: RBUser
) -> RBUser:
    """
    Add user to ldap

    Args:
        conn: LDAP connection to use
        smtp: SMTP client
        mailman: mailman Rest Client
        new_user: RBUser with all details of new user

    Return:
        If User is created successfully a RBUser will be returned with the new
        users details
    """

    await conn.add(new_user.dn, attributes=new_user.to_ldap())
    if not path.exists(new_user.home_directory):
        makedirs(new_user.home_directory, mode=0o711, exist_ok=True)
        with open(f"{new_user.home_directory}/.forward", "w+") as f:
            f.write(new_user.altmail)
        chown(new_user.home_directory, new_user.uid_number, new_user.gid_number)
    web_dir = f"/webtree/{new_user.uid[:1]}/{new_user.uid}"
    if not path.exists(web_dir):
        makedirs(web_dir, mode=0o755, exist_ok=True)
        chown(web_dir, new_user.uid_number, new_user.gid_number)
    symlink(web_dir, f"{new_user.home_directory}/public_html")
    chown(
        f"{new_user.home_directory}/public_html",
        new_user.uid_number,
        new_user.gid_number,
    )
    mailing_list = mailman.get_list("announce-redbrick")
    mailing_list.subscribe(f"{new_user.uid}@redbrick.dcu.ie")
    async with smtp:
        await smtp.send_account_details(
            new_user.altmail,
            new_user.uid,
            new_user.password,
            new_user.usertype,
            new_user.cn,
            new_user.id,
            new_user.course,
            new_user.year,
            new_user.newbie,
        )
    return new_user
