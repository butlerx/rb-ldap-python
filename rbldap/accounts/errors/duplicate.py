"""duplicate user excpetion"""


class DuplicateUser(Exception):
    """Exception for if a user with a username already exists"""

    msg = "User Already exists"
