from rbldap.commands import search


async def test_search():
    """
    test search function
    """
    res = await search(None, None)


async def test_search_dcu_id():
    """
    test search command with dcu id
    """
    res = await search(None, None)
