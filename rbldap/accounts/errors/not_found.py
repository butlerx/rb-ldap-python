"""user not found error"""


class UserNotFound(Exception):
    """Exception for when a user cant be found"""

    msg = "no user found"
