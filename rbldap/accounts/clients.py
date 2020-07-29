"""ldap client"""

from asyncio import AbstractEventLoop, get_event_loop
from contextlib import asynccontextmanager
from functools import partial
from typing import Any, AsyncGenerator, Dict, List, Tuple, Union

from ldap3 import ALL, ASYNC, SIMPLE, Connection, Server

__all__ = ["LDAPConnection", "Result"]

Controls = List[tuple]
ChangeSet = Dict[str, List[Tuple[str, list]]]
Result = Dict[str, Union[int, str, list]]


class LDAPConnection:
    """
    LDAP connection async wrapper

    Wrapper for ldap3 to provide asyncio bindings similar to bonsai

    Args:
        host: ldap server hostname
        port: ldap server port number
        user: user dn to bind to ldap with
        password_file: location of file containing password on disk
        client_strategy: client_strategy to connect to ldap with. ASYNC or MOCK_ASYNC excepted
        server: A LDAP server to be used, eg mock server
    """

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password_file: str,
        *,
        client_strategy: str = ASYNC,
        server: Server = None,
        loop: AbstractEventLoop = None,
    ):
        self.server = server or Server(
            host=host, port=port, use_ssl=False, get_info=ALL
        )
        self.loop = loop or get_event_loop()
        with open(password_file, "r") as file:
            password = file.read().strip()

        self.connection = Connection(
            self.server,
            user=user,
            password=password,
            auto_bind="NONE",
            version=3,
            authentication=SIMPLE,
            client_strategy=client_strategy,
            auto_referrals=True,
            check_names=True,
            read_only=False,
            lazy=False,
        )

    async def wait_for(self, msg_id: str) -> None:
        await self.loop.run_in_executor(
            None, partial(self.connection.get_respone, msg_id)
        )

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator["LDAPConnection", None]:
        """
        connect to ldap
        """
        try:
            self.connection.bind()
            yield self
        finally:
            self.connection.unbind()

    async def add(self, *args: Any, **kwargs: Any) -> Result:
        """
        Async Add LDAP Entry

        ref: https://ldap3.readthedocs.io/en/latest/add.html
        """
        await self.wait_for(self.connection.add(*args, **kwargs))
        return self.connection.results

    async def delete(self, *args: Any, **kwargs: Any) -> Result:
        """
        Async Delete LDAP Entry

        ref: https://ldap3.readthedocs.io/en/latest/delete.html
        """
        await self.wait_for(self.connection.delete(*args, *kwargs))
        return self.connection.results

    async def modify(self, *args: Any, **kwargs: Any) -> Result:
        """
        Async Modify ldap entry

        ref: https://ldap3.readthedocs.io/en/latest/modify.html
        """
        await self.wait_for(self.connection.modify(*args, *kwargs))
        return self.connection.results

    async def modify_dn(self, *args: Any, **kwargs: Any) -> Result:
        """
        Async Modify ldap entry

        ref: https://ldap3.readthedocs.io/en/latest/modifydn.html
        """
        await self.wait_for(self.connection.modify(*args, *kwargs))
        return self.connection.results

    async def search(self, *args: Any, **kwargs: Any) -> List[dict]:
        """
        Async Search ldap entry

        ref: https://ldap3.readthedocs.io/en/latest/searches.html
        """
        await self.wait_for(self.connection.search(*args, **kwargs))
        return self.connection.response
