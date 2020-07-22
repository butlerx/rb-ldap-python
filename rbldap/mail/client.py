"""custom mail client"""

from aiosmtplib import SMTP

from ..accounts.types import RBUser
from .account_details import account_details
from .alert_unpaid import unpaid_alert
from .password_reset import password_reset


class RBMail(SMTP):
    """Wrapper around smtp to add redbrick specific calls"""

    async def send_message(self, *args, **kwargs):
        """ensure starttls is called on all messages"""
        await self.starttls()
        return super().send_message(*args, **kwargs)

    async def send_account_details(self, user: RBUser):
        """
        Email a user their account details

        Args:
            user: the user to email and the details to email them
        """
        await self.send_message(account_details(user))

    async def send_password_reset(self, email: str, username: str, password: str):
        """
        Email User to inform them the password has been reset and what the password is

        Args:
            email: address to send email to
            username: account details
            password: new password
        """
        await self.send_message(password_reset(email, username, password))

    async def send_unpaid_alert(
        self, username: str, years_paid: int, altmail: str, fullname: str, dcu_id: int
    ):
        """
        Email User to inform them the password has been reset and what the password is

        Args:
            username: account to let know
            years_paid: number of years unpaid they are
            altmail: alternative email to conntact
            fullname: users name
            dcu_id: student id number
        """
        await self.send_message(
            unpaid_alert(username, years_paid, altmail, fullname, dcu_id)
        )
