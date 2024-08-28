import os
import typing as tp
from contextlib import asynccontextmanager

import asyncpg

DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER_PASSWORD = os.environ["DB_USER_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]


class DB:
    """A class responsible for database connections."""

    def __init__(
        self,
        database: str,
        user: str = "postgres",
        host: str = "localhost",
        port: str = "5432",
        password: str = "",
    ) -> None:
        """Init db connection."""
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        self.database = database
        self._connection_pool = None
        self._connection = None

    async def get_connection_pool(self) -> asyncpg.pool.Pool:
        """Returns a connection pool. Inits the pool if it hasn't been initialized yet."""
        if not self._connection_pool:
            connection_pool = await asyncpg.create_pool(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                command_timeout=60,
            )
            self._connection_pool = connection_pool
        return self._connection_pool

    @asynccontextmanager
    async def get_connection(self) -> tp.AsyncGenerator[asyncpg.Connection, None]:
        """Returns a connection from the pool. Releases it afterwords."""
        pool = await self.get_connection_pool()
        async with pool.acquire() as conn:
            yield conn
        await pool.release(conn)

    async def close(self) -> None:
        """Closes the connection pool."""
        if self._connection_pool:
            await self._connection_pool.close()


db = DB(
    user=DB_USER,
    host=DB_HOST,
    port=DB_PORT,
    password=DB_USER_PASSWORD,
    database=DB_NAME,
)
