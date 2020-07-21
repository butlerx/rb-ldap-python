"""custom mail client"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from markdown import markdown

from .accounts.types import RBUser


class RBMail(SMTP):
    """Wrapper around smtp to add redbrick specific calls"""

    async def email_account_details(self, user: RBUser):
        """
        Email a user their account details

        Args:
            user: the user to email and the details to email them
        """
        message = MIMEMultipart("alternative")
        message["From"] = "admin-request@redbrick.dcu.ie"
        message["To"] = user.altmail
        message["Subject"] = "Welcome to Redbrick! - Your Account Details"

        welcome_msg = (
            "Welcome to Redbrick, the DCU Networking Society! Thank you for joining."
            if user.newbie
            else "Welcome back to Redbrick, the DCU Networking Society! Thank you for renewing."
        )
        markdown_msg = f"""{welcome_msg}
Your Redbrick Account details are:

- username: {user.uid}
- password: {user.user_password}
- account type: {user.usertype}
- name: {user.cn}
- id number: {user.id}
- course: {user.course}
- year: {user.year}

---
Your Redbrick webpage: [{user.uid}.redbrick.dcu.ie](https://{user.uid}.redbrick.dcu.ie)
Your Redbrick email: {user.uid}@redbrick.dcu.ie
You can find out more about our services [here](https://www.redbrick.dcu.ie/about/welcome)

We recommend that you change your password as soon as you login.

Problems with your password or wish to change your username? Contact:
[admin-request@redbrick.dcu.ie](mailto:admin-request@redbrick.dcu.ie)

Problems using Redbrick in general or not sure what to do? Contact:
[helpdesk-request@redbrick.dcu.ie](mailto:helpdesk-request@redbrick.dcu.ie)

Have fun!

- Redbrick Admin Team"""

        message.attach(MIMEText(markdown_msg, "plain", "utf-8"))
        message.attach(MIMEText(markdown(markdown_msg), "html", "utf-8"))
        await self.starttls()
        await self.send_message(message)
