"""search command"""

from ..accounts import search_dcu, search_rb


async def search(args):
    if args.dcu:
        print(search_dcu(args))
    else:
        print(search_rb(args))
