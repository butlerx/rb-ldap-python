"""Redbrick ldap search"""


def search_rb_cli(args):
    """cli interface for searchong redbrick ldap"""


def search_rb(
    ldap_conn,
    uid: str = None,
    dcu_id: str = None,
    altmail: str = None,
    fullname: str = None,
):
    """Seach RB ldap for user"""
