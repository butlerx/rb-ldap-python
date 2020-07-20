"""delete unpaid automation"""


async def delete_unpaid():
    """
    Delete all unpaid users accounts that are outside their grace period (years paid = -1)
    """
