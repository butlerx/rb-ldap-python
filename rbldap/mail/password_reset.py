"""acount details message"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from markdown import markdown


def password_reset(email: str, username: str, password: str) -> MIMEMultipart:
    """
    Format email for user password reset

    Args:
        email: address to send email to
        username: account details
        password: new password

    Returns:
        Formatted Message containg html and plaintext
    """
    message = MIMEMultipart("alternative")
    message["From"] = "admin-request@redbrick.dcu.ie"
    message["To"] = email
    message["Subject"] = "Account Password Reset"
    markdown_msg = f"""Hello {username}.
Your Redbriock Account's password has been reset.

Your new Password is {password}

We recommend that you change your password as soon as you login.

Problems with your password or wish to change your username? Contact:
[admin-request@redbrick.dcu.ie](mailto:admin-request@redbrick.dcu.ie)

Problems using Redbrick in general or not sure what to do? Contact:
[helpdesk-request@redbrick.dcu.ie](mailto:helpdesk-request@redbrick.dcu.ie)

- Redbrick Admin Team"""

    message.attach(MIMEText(markdown_msg, "plain", "utf-8"))
    message.attach(MIMEText(markdown(markdown_msg), "html", "utf-8"))
    return message
