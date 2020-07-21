"""generate vhost config"""
import os.path
import sys

from bonsai import LDAPClient

from ..accounts import gid_to_usertype


def user2nix(uid: str, home: str, gid: str) -> str:
    return f"""  {{
    uid = "{uid}";',
    home = "{home}";',
    gid = "{gid}";',
  }}"""


async def generate(rb_client: LDAPClient, output: str, *, webtree: str = "/webtree"):
    """
    Generate nix config for user vhosts based off ldap

    Args:
        rb_client: ldap client configured for redbrick ldap
        output: path to write generate config too
        webtree: Root folder of webtree
    """
    num_users = 0
    nix = []

    async with rb_client.connect(is_async=True) as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(objectclass=posixAccount)",
            attrlist=["uid", "homeDirectory", "gidNumber"],
        )
    for user in res:
        uid = user["uid"][0]
        home = user["homeDirectory"][0]
        gid = gid_to_usertype(user["gidNumber"][0])

        if uid and home and gid:
            if os.path.exists(f"{webtree}/{uid[0]}/{uid}") or "/var/lib" in home:
                nix.append(user2nix(uid=uid, home=home, gid=gid))
                num_users += 1
            else:
                print(f"Skipping {uid}: missing webtree")

    print(f"Generated nix config for {str(num_users)} users")
    nix_conf = "\n".join(nix)
    with open(output, "w+") as f:
        f.write(f"[\n{nix_conf}\n]")
    return 0
