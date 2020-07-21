"""dcu id excpetion"""


class UnknownID(Exception):
    """Exception for the id beeing queried with is unrecognised"""

    msg = "Given id does not match any"
