"""custom mail client"""

from aiosmtplib import SMTP

from .account_details import account_details
from .alert_unpaid import unpaid_alert
from .password_reset import password_reset

__all__ = ["RBMail"]


class RBMail(SMTP):
    """Wrapper around smtp to add redbrick specific calls"""

    async def send_message(self, *args, **kwargs):
        """
        ensure starttls is called on all messages

        Args:
            email: address to send details too
            uid: username of the user
            password: users password
            usertype: users usertype
            name: full name of user
            id: student id of user
            course: students course
            year: studets year
            newbie: if they are a new user
        """
        await self.starttls()
        return super().send_message(*args, **kwargs)

    async def send_account_details(self, *args, **kwargs):
        """
        Email a user their account details

        Args:
            user: the user to email and the details to email them
        """
        await self.send_message(account_details(*args, **kwargs))

    async def send_password_reset(self, *args, **kwargs):
        """
        Email User to inform them the password has been reset and what the password is

        Args:
            email: address to send email to
            username: account details
            password: new password
        """
        await self.send_message(password_reset(*args, **kwargs))

    async def send_unpaid_alert(self, *args, **kwargs):
        """
        Email User to inform them the password has been reset and what the password is

        Args:
            username: account to let know
            years_paid: number of years unpaid they are
            altmail: alternative email to conntact
            fullname: users name
            dcu_id: student id number
        """
        await self.send_message(unpaid_alert(*args, **kwargs))
