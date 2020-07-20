"""search command"""

from bonsai import LDAPClient

from ..accounts import search_dcu, search_rb
from ..fs import read_file_to_string


async def search(args):
    """search for a user"""
    if args.dcu:
        client = LDAPClient(f"ldap://{args.dcu_host}")
        client.set_credentials(
            "SIMPLE",
            user=args.dcu_user,
            password=read_file_to_string(args.dcu_password),
        )
        async with client.connect(is_async=True) as conn:
            results = await search_dcu(
                conn, dcu_id=args.id, uid=args.uid, fullname=args.fullname
            )
            print("No User found" if not results else results)
    else:
        client = LDAPClient(f"ldap://{args.host}")
        client.set_credentials(
            "SIMPLE", user=args.user, password=read_file_to_string(args.password)
        )
        async with client.connect(is_async=True) as conn:
            results = await search_rb(
                conn,
                uid=args.uid,
                dcu_id=args.id,
                altmail=args.altmail,
                fullname=args.fullname,
                noob=args.nood,
            )
            print("No User found" if not results else results)
