"""unpaid user alert"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from markdown import markdown


def unpaid_alert(
    username: str, years_paid: int, altmail: str, fullname: str, dcu_id: int
) -> MIMEMultipart:
    """
    Format email to alert user there account is unpaid

    Args:
        username: account to let know
        years_paid: number of years unpaid they are
        altmail: alternative email to conntact
        fullname: users name
        dcu_id: student id number

    Returns:
        Formatted Message containg html and plaintext
    """
    message = MIMEMultipart("alternative")
    message["From"] = "accounts@redbrick.dcu.ie"
    message["To"] = f"{username}@redbrick.dcu.ie"
    message["Cc"] = altmail
    message["Subject"] = "Time to renew your Redbrick account!"

    warning = (
        """
If you do not renew within the following month, your account will be disabled
Your account will remain on the system for a grace period of a year - you
just won't be able to login. So don't worry, it won't be deleted any time
soon! You can renew at any time during the year.
"""
        if years_paid == 0
        else """
If you do not renew within the following month, your account WILL BE
DELETED at the start of the new year. This is because you were not
recorded as having paid for last year and as such are nearing the end of
your one year 'grace' period to renew. Please make sure to renew as soon
as possible otherwise please contact us at: [accounts@redbrick.dcu.ie](mailto:accounts@redbrick.dcu.ie).
"""
    )

    email = f"""Hey there,
It's that time again to renew your Redbrick account!
Membership prices, as set by the SLC, are as follows:

```
Members      EUR 4
Associates   EUR 8
Staff        EUR 8
Guests       EUR 10
```

Note: if you have left DCU, you need to apply for associate membership.
You can pay in person, by lodging money into our account, electronic bank
transfer, or even PayPal! All the details you need are [here](https://www.redbrick.dcu.ie/help/joining)

Our bank details are:
```
a/c name: DCU Redbrick Society
IBAN: IE59BOFI90675027999600
BIC: BOFIIE2D
a/c number: 27999600
sort code: 90 - 67 - 50
```

Please Note!

{warning}

If in fact you have renewed and have received this email in error, it is
important you let us know. Just reply to this email and tell us how and
when you renewed and we'll sort it out.
For your information, your current Redbrick account details are:

username: {username}
name: {fullname}
alternative email: {altmail}
id number: {dcu_id}

If any of the above details are wrong, please correct them when you
renew!
- Redbrick Admin Team
"""

    message.attach(MIMEText(email, "plain", "utf-8"))
    message.attach(MIMEText(markdown(email), "html", "utf-8"))
    return message
