"""mocked interfaces"""
from contextlib import asynccontextmanager
from email.mime.multipart import MIMEMultipart
from typing import AsyncGenerator, List

import pytest
from ldap3 import MOCK_ASYNC, Server
from mailmanclient import Client

import rbldap.mail
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
        password_file="./tests/assets/password_file.secret",
        server=Server("redbrick ldap mock"),
        client_strategy=MOCK_ASYNC,
    )
    ldap.connection.strategy.entries_from_json("./tests/assets/redbrick_entries.json")
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
        password_file="./tests/assets/password_file.secret",
        server=Server("dcu ldap mock"),
        client_strategy=MOCK_ASYNC,
    )
    ldap.connection.strategy.entries_from_json("./tests/assets/dcu_entries.json")
    return ldap


class DummySMTP:
    """SMTP mocked interface"""

    def __init__(self) -> None:
        self.sent_mail: List[MIMEMultipart] = []
        self.has_quit = False

    async def starttls(self) -> None:
        pass

    async def send_message(self, message: MIMEMultipart) -> None:
        """ensure starttls is called on all messages"""
        self.sent_mail.append(message)

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator["DummySMTP", None]:
        """mock connecting to ldap"""
        try:
            yield self
        finally:
            self.has_quit = True


@pytest.fixture
def smtp() -> rbldap.mail.RBMail:
    """
    create smtp client
    This is a Monkeypatch

    Retruns:
        SMTP client that mocks sending email
    """
    # Sure i might be a terrible person but lets see you mock an smtp server
    rbldap.mail.SMTP = DummySMTP
    return rbldap.mail.RBMail()


@pytest.fixture
def mailman() -> Client:
    """
    create mocked mailman client

    Returns:
        mailman client with mock interface
    """
