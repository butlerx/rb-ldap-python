"""Redbrick ldap search"""

from bonsai.ldapconnection import LDAPConnection


async def search_rb(
    ldap_conn: LDAPConnection,
    uid: str = None,
    dcu_id: str = None,
    altmail: str = None,
    fullname: str = None,
):
    """Seach RB ldap for user"""
