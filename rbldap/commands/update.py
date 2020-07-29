"""update command"""

from ..accounts.clients import LDAPConnection
from ..mail import RBMail


async def update(
    rb_client: LDAPConnection,
    dcu_client: LDAPConnection,
    smtp_client: RBMail,
    commit: bool,
    username: str,
):
    """
    Update a user in ldap

    Args:
        rb_client: ldap client configured for redbrick ldap
        dcu_client: ldap client configured for dcu AD
        smtp_client: redbrick smtp client
        commit: flag to commit any changes
        username: account to be updated

    Returns:
        Returns int to indicate exit code

    Raises:
        UserNotFound: raised if the user is not found
    """
