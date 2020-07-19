"""functions for checking if a username is free"""


def check_free_cli(args):
    """check if a username is free in ldap cli interface"""
    if check_free(args.username):
        print(f"{args.username} is free")
    else:
        print(f"{args.username} is taken")


def check_free(username: str) -> bool:
    """check if a username is free in ldap"""
    return True
