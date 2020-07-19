"""rbldap entrypoint"""
from argparse import ArgumentParser
from asyncio import get_event_loop

from .commands import (
    add,
    alert_unpaid,
    delete_unpaid,
    disable,
    disable_unpaid,
    enable,
    free,
    new_year,
    renew,
    reset_password,
    reset_shell,
    search,
    update,
)
from .version import PACKAGE_INFO, __author__, __version__


def parse_args():
    """parse commandline Interface"""
    parser = ArgumentParser(description=PACKAGE_INFO, epilog=f"Built by {__author__}")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--user",
        default="cn=root,ou=ldap,o=redbrick",
        help="ldap user, used for authentication",
        type=str,
    )
    parser.add_argument(
        "--dcu-user",
        help="Active Directory user for DCU, used for authentication",
        default="CN=rblookup,OU=Service Accounts,DC=ad,DC=dcu,DC=ie",
        type=str,
    )
    parser.add_argument(
        "--host", help="ldap host to query", default="ldap.internal", type=str
    )
    parser.add_argument(
        "--dcu-host",
        help="DCU Active Directory host to query",
        default="ad.dcu.ie",
        type=str,
    )
    parser.add_argument("--port", help="Port for ldap host", default=389, type=int)
    parser.add_argument(
        "--dcu-port", help="Port for DCU Active Directory host", default=389, type=int
    )
    parser.add_argument(
        "--password",
        help="password for the ldap server",
        default="/etc/ldap.secret",
        type=str,
    )
    parser.add_argument(
        "--dcu-password",
        help="password for the DCU ldap server",
        default="/etc/dcu_ldap.secret",
        type=str,
    )
    parser.add_argument(
        "--smtp",
        help="smtp server to send email with",
        default="smtp.redbrick.dcu.ie",
        type=str,
    )
    parser.add_argument(
        "--dry-run", help="output to console rather then file", action="store_true"
    )
    subparsers = parser.add_subparsers()

    search_parser = subparsers.add_parser("search", help="Search ldap for user")
    search_parser.add_argument("--altmail", help="Users email address", type=str)
    search_parser.add_argument("--uid", help="Users username", type=str)
    search_parser.add_argument("--id", help="DCU id Number", type=str)
    search_parser.add_argument("--fullname", help="User's fullname", type=str)
    search_parser.add_argument(
        "--noob", help="filter for new users", action="store_true"
    )
    search_parser.add_argument(
        "--dcu", help="Query DCU Active Directory", action="store_true"
    )
    search_parser.set_defaults(func=search)

    free_parser = subparsers.add_parser("free", help="check if a username is free")
    free_parser.add_argument("username", type=str)
    free_parser.set_defaults(func=free)

    add_parser = subparsers.add_parser("add", help="Add user to ldap")
    add_parser.add_argument("username", type=str)
    add_parser.set_defaults(func=add)

    disable_parser = subparsers.add_parser(
        "disable", help="Disable a Users ldap account"
    )
    disable_parser.add_argument("username", type=str)
    disable_parser.set_defaults(func=disable)

    enable_parser = subparsers.add_parser("enable", help="Renable a Users ldap account")
    enable_parser.add_argument("username", type=str)
    enable_parser.set_defaults(func=enable)

    renew_parser = subparsers.add_parser("renew", help="renew a LDAP user")
    renew_parser.add_argument("username", type=str)
    renew_parser.set_defaults(func=renew)

    reset_parser = subparsers.add_parser("reset", help="reset a users password")
    reset_parser.add_argument("username", type=str)
    reset_parser.set_defaults(func=reset_password)

    reset_shell_parser = subparsers.add_parser(
        "reset-shell", help="reset a users shell"
    )
    reset_shell_parser.add_argument("username", type=str)
    reset_shell_parser.set_defaults(func=reset_shell)

    update_parser = subparsers.add_parser("update", help="Update a user in ldap")
    update_parser.add_argument("username", type=str)
    update_parser.set_defaults(func=update)

    # Batch commands
    subparsers.add_parser(
        "alert-unpaid",
        help="Alert all unpaid users that their accounts will be disabled",
        func=alert_unpaid,
    )
    subparsers.add_parser(
        "delete-unpaid",
        help="Delete all unpaid users accounts that are outside their grace period",
        func=delete_unpaid,
    )

    subparsers.add_parser(
        "disable-unpaid", help="Diable all unpaid users accounts", func=disable_unpaid
    )

    subparsers.add_parser(
        "new-year",
        help="Decriment Years Paid of all users to 1",
        description="Migrate all users to no longer be marked as newbies and mark all users as unpaided. To Be run at the beginning of each year prior to C&S",
        func=new_year,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    loop = get_event_loop()
    loop.run_until_complete(args.func(args))
