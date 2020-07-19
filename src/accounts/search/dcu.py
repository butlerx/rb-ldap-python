"""dcu ldap search"""

from bonsai.ldapconnection import LDAPConnection


async def search_dcu(conn: LDAPConnection, dcu_id: str = None, fullname: str = None):
    """Seach DCU ldap for user"""
