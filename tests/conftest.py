import pytest

from ldap3 import MOCK_ASYNC, Connection, Server
from rbldap.accounts.clients import LDAPConnection


@pytest.fixture
def rb_ldap() -> LDAPConnection:
    """
    create mocked ldap connection for redbrick

    Returns:
        LDAPConnection for use in tests with ldap server setup
    """
    ldap = LDAPConnection(
        "mocked",
        389,
        user="cn=root,ou=ldap,o=redbrick",
        password_file="password_file.secret",
        server=Server("redbrick ldap mock"),
        client_strategy=MOCK_ASYNC,
    )
    ldap.connection.strategy.entries_from_json("redbrick_entries.json")
    return ldap


@pytest.fixture
def dcu_ldap() -> LDAPConnection:
    """
    create mocked ldap connection for dcu

    Returns:
        LDAPConnection for use in tests with ldap server setup
    """
    ldap = LDAPConnection(
        "mocked",
        389,
        user="CN=rblookup,OU=Service Accounts,DC=ad,DC=dcu,DC=ie",
        password_file="password_file.secret",
        server=Server("dcu ldap mock"),
        client_strategy=MOCK_ASYNC,
    )
    ldap.connection.strategy.entries_from_json("dcu_entries.json")
    return ldap
