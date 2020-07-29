import pytest
from mailmanclient import Client

from rbldap.accounts.clients import LDAPConnection
from rbldap.commands import new_year


@pytest.mark.asyncio
async def test_new_year_i_dont_know_what_im_doing(
    rb_ldap: LDAPConnection, mailman: Client
) -> None:
    """
    test new year command where user doent know what they are doing
    """
    res = await new_year(rb_ldap, mailman, True)
    assert res == 1
    # TODO check that ldap is still in same state


@pytest.mark.asyncio
async def test_new_year_i_know_what_im_doing(
    rb_ldap: LDAPConnection, mailman: Client
) -> None:
    """
    test new year command where user doent know what they are doing
    """
    res = await new_year(rb_ldap, mailman, True, i_know_what_im_doing=True)
    assert res == 0
    # TODO check that ldap has been updated
