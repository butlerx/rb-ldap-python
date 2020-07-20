"""new year automation"""


def new_year():
    """
    To Be run at the beginning of each year prior to C&S
    Preform yearly update:
      - Set newbie to false
      - Decriment Years Paid of all users by 1
      - Disable all accounts with years paid at 0.
      - Delete all accounts with years paid of -1
    """
