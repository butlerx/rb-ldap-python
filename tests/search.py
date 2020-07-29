import pytest

from rbldap.accounts.clients import LDAPConnection
from rbldap.commands import search


@pytest.mark.asyncio
async def test_search(rb_ldap: LDAPConnection, dcu_ldap: LDAPConnection) -> None:
    """
    test search function
    """
    res = await search(rb_ldap, dcu_ldap)
    assert not res


@pytest.mark.asyncio
async def test_search_dcu_id(rb_ldap: LDAPConnection, dcu_ldap: LDAPConnection) -> None:
    """
    test search command with dcu id
    """
    res = await search(rb_ldap, dcu_ldap)
    assert not res
