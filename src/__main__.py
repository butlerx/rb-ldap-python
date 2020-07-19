"""rbldap entrypoint"""
from argparse import ArgumentParser

from .add import add_user_cli
from .batch import (
    alert_unpaid_users_cli,
    delete_unpaid_users_cli,
    disable_unpaid_users_cli,
    new_year_cli,
)
from .disable import disable_user_cli
from .enable import enable_user_cli
from .free import check_free_cli
from .renew import renew_user_cli
from .reset import reset_password_cli, reset_shell_cli
from .search import search_dcu_cli, search_rb_cli
from .update import update_user_cli
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

    search = subparsers.add_parser("search", help="Search ldap for user")
    search.add_argument("--altmail", help="Users email address", type=str)
    search.add_argument("--uid", help="Users username", type=str)
    search.add_argument("--id", help="DCU id Number", type=str)
    search.add_argument("--fullname", help="User's fullname", type=str)
    search.add_argument("--noob", help="filter for new users", action="store_true")
    search.add_argument("--dcu", help="Query DCU Active Directory", action="store_true")
    search.set_defaults(
        func=lambda args: search_dcu_cli(args) if args.dcu else search_rb_cli(args)
    )

    free = subparsers.add_parser("free", help="check if a username is free")
    free.add_argument("username", type=str)
    free.set_defaults(func=check_free_cli)

    add = subparsers.add_parser("add", help="Add user to ldap")
    add.add_argument("username", type=str)
    add.set_defaults(func=add_user_cli)

    disable = subparsers.add_parser("disable", help="Disable a Users ldap account")
    disable.add_argument("username", type=str)
    disable.set_defaults(func=disable_user_cli)

    renable = subparsers.add_parser("renable", help="Renable a Users ldap account")
    renable.add_argument("username", type=str)
    renable.set_defaults(func=enable_user_cli)

    renew = subparsers.add_parser("renew", help="renew a LDAP user")
    renew.add_argument("username", type=str)
    renew.set_defaults(func=renew_user_cli)

    reset_pass = subparsers.add_parser("reset", help="reset a users password")
    reset_pass.add_argument("username", type=str)
    reset_pass.set_defaults(func=reset_password_cli)

    reset_shell = subparsers.add_parser("reset-shell", help="reset a users shell")
    reset_shell.add_argument("username", type=str)
    reset_shell.set_defaults(func=reset_shell_cli)

    update = subparsers.add_parser("update", help="Update a user in ldap")
    update.add_argument("username", type=str)
    update.set_defaults(func=update_user_cli)

    # Batch commands
    alert_unpaid = subparsers.add_parser(
        "alert-unpaid",
        help="Alert all unpaid users that their accounts will be disabled",
    )
    alert_unpaid.set_defaults(func=alert_unpaid_users_cli)

    delete_unpaid = subparsers.add_parser(
        "delete-unpaid",
        help="Delete all unpaid users accounts that are outside their grace period",
    )
    delete_unpaid.set_defaults(func=delete_unpaid_users_cli)

    disable_unpaid = subparsers.add_parser(
        "disable-unpaid", help="Diable all unpaid users accounts"
    )
    disable_unpaid.set_defaults(func=disable_unpaid_users_cli)

    new_year = subparsers.add_parser(
        "new-year",
        help="Decriment Years Paid of all users to 1",
        description="Migrate all users to no longer be marked as newbies and mark all users as unpaided. To Be run at the beginning of each year prior to C&S",
    )
    new_year.set_defaults(func=new_year_cli)

    return parser.parse_args()


if __name__ == "__main__":
    ARGS = parse_args()
    ARGS.func(ARGS)
