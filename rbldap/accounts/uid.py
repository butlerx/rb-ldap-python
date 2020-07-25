"""uid functions"""

from .clients import LDAPConnection


async def find_available_uid(ldap_conn: LDAPConnection) -> int:
    """
    Seach RB ldap for next available uid

    Args:
        ldap_conn: LDAP connection to use for searching

    Returns:
        next avilable uid
    """
    res = await ldap_conn.search(
        "ou=accounts,o=redbrick",
        "(objectclass=posixAccount)",
        attributes=["uidNumber"],
    )
    uids = [entry["attributes"]["uidNumber"][0] for entry in res]
    uids.sort()
    return int(uids[-1]) + 1
