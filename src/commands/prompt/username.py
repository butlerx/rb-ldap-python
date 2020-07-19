"""functions to prompt user"""
def get_username(username: str = None) -> str:
    """prompt user for username if none given"""
    if not username:
        return input("Enter username: ")
    return username
