from typing import Any, Optional

from src.infra.repositories.db.db_base import DBBaseRepository
from src.infra.repositories.db.exceptions import EntityNotFoundException
from src.infra.repositories.db.model import (
    Bot,
    DBCreateBotParams,
)


class DBBotRepository(DBBaseRepository):
    @property
    def _model_cls(self):
        return Bot

    @property
    def _query(self):
        return f"SELECT bot_id, token, date_created from {self.db_schema}.bots"

    async def get_one(self, id: Any) -> _model_cls:
        query = f"{self._query} where id = :id"
        res = await self.one_query(query, {"id": id})
        if not res:
            raise EntityNotFoundException
        return res

    async def get_by_bot_id(self, bot_id: str) -> _model_cls:
        query = f"{self._query} where bot_id = :bot_id"
        res = await self.one_query(query, {"bot_id": bot_id})
        if not res:
            raise EntityNotFoundException
        return res

    async def get_by_token(self, token: str) -> _model_cls:
        query = f"{self._query} where token = :token"
        res = await self.one_query(query, {"token": token})
        if not res:
            raise EntityNotFoundException
        return res

    async def delete_by_bot_id(self, bot_id: str) -> _model_cls:
        query = f"DELETE FROM {self.db_schema}.bots WHERE bot_id = :bot_id RETURNING *"
        res = await self.one_query(query, {"bot_id": bot_id})
        if not res:
            raise EntityNotFoundException
        return res

    async def delete_by_bot_token(self, token: str) -> _model_cls:
        query = f"DELETE FROM {self.db_schema}.bots WHERE token = :token RETURNING *"
        res = await self.one_query(query, {"bot_id": token})
        if not res:
            raise EntityNotFoundException
        return res

    async def get_many(self, limit: int, offset: int) -> Optional[list[_model_cls]]:
        query = f"SELECT bot_id, token, date_created from {self.db_schema}.bots ORDER BY date_created LIMIT {limit} OFFSET {offset}"
        return await self.all_query(query)

    async def delete(self, id: Any) -> _model_cls:
        query = f"DELETE FROM {self.db_schema}.users WHERE id = :id RETURNING *"
        res = await self.one_query(query, {"id": id})
        if not res:
            raise EntityNotFoundException
        return res

    async def create(self, params: DBCreateBotParams) -> _model_cls:
        keys = ", ".join([k for k in params.dict().keys()])
        kkeys = ", ".join([f":{k}" for k in params.dict().keys()])
        print("ALL KEYS", params.dict().keys())
        print("KEYS", keys)
        query = (
            f"INSERT INTO {self.db_schema}.bots ({keys}) VALUES ({kkeys}) RETURNING *"
        )
        return await self.one_query(query, params.dict())

    # async def update(self, id: Any, params: UpdateUserParams) -> _model_cls:
    #     upd_datams = ", ".join(
    #         [f"{k} = :{k}" for k in params.dict(exclude_unset=True).keys()]
    #     )
    #     query = (
    #         f"UPDATE {self.db_schema}.users SET {upd_datams} WHERE id = :id RETURNING *"
    #     )
    #     return await self.one_query(query, params.dict(exclude_unset=True) | {"id": id})
    #
    async def get_row_count(self) -> int:
        return await self.get_value(f"SELECT count(0) FROM {self.db_schema}.bots")
