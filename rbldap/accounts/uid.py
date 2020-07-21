"""uid functions"""

from bonsai.ldapconnection import LDAPConnection


async def find_available_uid(ldap_conn: LDAPConnection) -> int:
    """
    Seach RB ldap for next available uid

    Args:
        ldap_conn: LDAP connection to use for searching

    Returns:
        next avilable uid
    """
    res = await ldap_conn.search(
        "ou=accounts,o=redbrick", 2, "(&)", attrlist=["uidNumber"]
    )
    uids = [entry["uidNumber"][0] for entry in res]
    uids.sort()
    return uids[-1] + 1
