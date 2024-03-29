"""rbldap entrypoint"""

from mailmanclient import Client

from . import __author__, __doc__, __version__
from .accounts.clients import LDAPConnection
from .cli_parser import Program
from .commands import (
    add,
    alert_unpaid,
    delete_unpaid,
    disable,
    disable_unpaid,
    enable,
    free,
    generate,
    new_year,
    renew,
    reset_password,
    reset_shell,
    search,
    update,
)
from .mail import RBMail


def build_globals(
    *,
    user: str = "cn=root,ou=ldap,o=redbrick",
    dcu_user: str = "CN=rblookup,OU=Service Accounts,DC=ad,DC=dcu,DC=ie",
    host: str = "ldap.internal",
    dcu_host: str = "ad.dcu.ie",
    port: int = 389,
    dcu_port: int = 389,
    password: str = "/var/secrets/ldap.secret",
    dcu_password: str = "/var/secrets/dcu_ldap.secret",
    smtp: str = "smtp.redbrick.dcu.ie",
    dry_run: bool = False,
    mailman_host: str = "https://lists.redbrick.dcu.ie/3.1",
    mailman_user: str = "admin",
    mailman_password: str = "/var/secrets/mailman.secret",
) -> dict:
    """
    Setup Shared clients

    Args:
        user: ldap user, used for authentication
        dcu_user: Active Directory user for DCU, used for authentication
        host: ldap host to query
        dcu_host: DCU Active Directory host to query
        port: Port for ldap host
        dcu_port: Port for DCU Active Directory host
        password: path to file containing the password for the ldap server
        dcu_password: path to file containing the password for the DCU AD server"
        smtp: smtp server to send email with
        dry_run: output to console rather then file
        mailman_host: url to mailman server
        mailman_user: user account to use with mailman
        mailman_password: secret file to use for mailman password

    Returns:
        Dictionary of objects that can be accessed from commads
    """
    with open(mailman_password, "r") as file:
        _mailman_password = file.read().strip()

    return dict(
        rb_client=LDAPConnection(host, port, user, password),
        dcu_client=LDAPConnection(dcu_host, dcu_port, dcu_user, dcu_password),
        smtp_client=RBMail(hostname=smtp, port=587, use_tls=False),
        mailman=Client(mailman_host, mailman_user, _mailman_password),
        commit=(not dry_run),
    )


if __name__ == "__main__":
    Program(
        prog="rb-ldap",
        description=__doc__,
        version=__version__,
        author=__author__,
        bootstrap=build_globals,
        bootstrap_resv=["rb_client", "dcu_client", "smtp_client", "mailman", "commit"],
    ).add_commands(
        add,
        search,
        renew,
        free,
        enable,
        disable,
        reset_password,
        reset_shell,
        update,
        generate,
    ).add_commands(
        # Batch Commands
        alert_unpaid,
        delete_unpaid,
        disable_unpaid,
        new_year,
    ).parse_args().run_command()
