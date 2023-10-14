from typing import Optional, Any, Union, Type

from aiopg import Transaction
from aiopg.sa import Engine, SAConnection
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from pydantic import BaseModel
from sqlalchemy import text

from src.infra.repositories.db.exceptions import EntityAlreadyExistsException


class DBBaseRepository:
    def __init__(self, db_schema: str, engine: Engine):
        self.db_schema = f'"{db_schema}"'
        self.engine = engine

    async def one_query(
        self, sql: str, binds: Optional[dict[str, Any]] = None
    ) -> Optional[Type[BaseModel]]:
        async with self.engine.acquire() as conn:
            result = await self._execute_query(conn, sql, binds)
        if result:
            return self._model_cls(**result[0])

    async def all_query(
        self, sql: str, binds: Optional[dict[str, Any]] = None
    ) -> Optional[list[Type[BaseModel]]]:
        async with self.engine.acquire() as conn:
            res = await self._execute_query(conn, sql, binds)
        return [self._model_cls(**row) for row in res]

    async def execute_query(
        self, sql: str, binds: Optional[dict[str, Any]] = None
    ) -> Optional[list[Type[BaseModel]]]:
        async with self.engine.acquire() as conn:
            return await self._execute_query(conn, sql, binds)

    async def get_value(self, sql: str) -> Union[str, int]:
        async with self.engine.acquire() as conn:
            result = await self._execute_query(conn, sql)
            return result[0][0]

    async def _execute_query(
        self, conn: Union[SAConnection, Transaction], query, binds=None
    ) -> list[Any]:
        try:
            if binds:
                r_ = await conn.execute(text(query), binds, returns_rows=True)
            else:
                r_ = await conn.execute(text(query), returns_rows=True)
            try:
                return await r_.fetchall()
            except:
                pass
        except errors.lookup(UNIQUE_VIOLATION):
            raise EntityAlreadyExistsException(details="Unique key constraint")
