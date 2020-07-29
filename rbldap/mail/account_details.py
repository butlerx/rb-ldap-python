"""acount details message"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from markdown import markdown


def account_details(
    email: str,
    uid: str,
    password: str,
    usertype: str,
    name: str,
    id: int,
    course: str,
    year: int,
    newbie: bool = False,
) -> MIMEMultipart:
    """
    Format user details for email

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

    Returns:
        Formatted Message containg html and plaintext
    """
    message = MIMEMultipart("alternative")
    message["From"] = "admin-request@redbrick.dcu.ie"
    message["To"] = email
    message["Subject"] = "Welcome to Redbrick! - Your Account Details"

    welcome_msg = (
        "Welcome to Redbrick, the DCU Networking Society! Thank you for joining."
        if newbie
        else "Welcome back to Redbrick, the DCU Networking Society! Thank you for renewing."
    )
    markdown_msg = f"""{welcome_msg}
Your Redbrick Account details are:

- username: {uid}
- password: {password}
- account type: {usertype}
- name: {name}
- id number: {id}
- course: {course}
- year: {year}

---
Your Redbrick webpage: [{uid}.redbrick.dcu.ie](https://{uid}.redbrick.dcu.ie)
Your Redbrick email: {uid}@redbrick.dcu.ie
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
    return message
