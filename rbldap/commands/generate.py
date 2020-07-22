"""generate vhost config"""
from os import path
from typing import Optional

from bonsai import LDAPClient

from ..accounts import gid_to_usertype


def user2nix(uid: str, home: str, gid: str) -> str:
    """
    Generate nix config for user vhosts based off ldap

    Args:
        uid: Username of user
        home: homedir of user
        gid: user type of user

    Returns:
        Returns String containing a nix object for inserting in a nix array
    """
    return f"""  {{
    uid = "{uid}";',
    home = "{home}";',
    gid = "{gid}";',
  }}"""


def ldap2nix(user: dict, webtree: str) -> Optional[str]:
    """
    Convert ldap entry to nix config

    Args:
        user: raw response from ldap client for user
        webtree: root webtree path
    Returns:
        Returns String containing a nix object for inserting in a nix array
    """
    uid = user["uid"][0]
    home = user["homeDirectory"][0]
    gid = gid_to_usertype(user["gidNumber"][0])

    if uid and home and gid:
        if path.exists(f"{webtree}/{uid[0]}/{uid}") or "/var/lib" in home:
            return user2nix(uid=uid, home=home, gid=gid)
        print(f"Skipping {uid}: missing webtree")
    return None


async def generate(rb_client: LDAPClient, output: str, *, webtree: str = "/webtree"):
    """
    Generate nix config for user vhosts based off ldap

    Args:
        rb_client: ldap client configured for redbrick ldap
        output: path to write generate config too
        webtree: Root folder of webtree
    """
    async with rb_client.connect(is_async=True) as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(objectclass=posixAccount)",
            attrlist=["uid", "homeDirectory", "gidNumber"],
        )
    nix = [
        conf for conf in [ldap2nix(user, webtree) for user in res] if conf is not None
    ]

    print(f"Generated nix config for {str(len(nix))} users")
    nix_conf = "\n".join(nix)
    with open(output, "w+") as f:
        f.write(f"[\n{nix_conf}\n]")
    return 0
