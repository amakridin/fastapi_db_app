from typing import Any, Optional

from src.infra.repositories.db.db_base import DBBaseRepository
from src.infra.repositories.db.exceptions import EntityNotFoundException
from src.infra.repositories.db.model import User, DBCreateUserParams, UpdateUserParams


class DBUserRepository(DBBaseRepository):
    @property
    def _model_cls(self):
        return User

    async def get_one(self, id: Any) -> User:
        query = f"SELECT id, name, locale from {self.db_schema}.users where id = :id"
        res = await self.one_query(query, {"id": id})
        if not res:
            raise EntityNotFoundException
        return res

    async def get_many(self, limit: int, offset: int) -> Optional[list[User]]:
        query = f"SELECT id, name, locale from {self.db_schema}.users ORDER BY date_created LIMIT {limit} OFFSET {offset}"
        return await self.all_query(query)

    async def delete(self, id: Any) -> User:
        query = f"DELETE FROM {self.db_schema}.users WHERE id = :id RETURNING *"
        res = await self.one_query(query, {"id": id})
        if not res:
            raise EntityNotFoundException
        return res

    async def create(self, params: DBCreateUserParams) -> User:
        query = f"INSERT INTO {self.db_schema}.users (name, locale) VALUES (:name, :locale) RETURNING *"
        return await self.one_query(query, params.dict())

    async def update(self, id: Any, params: UpdateUserParams) -> User:
        upd_datams = ", ".join(
            [f"{k} = :{k}" for k in params.dict(exclude_unset=True).keys()]
        )
        query = (
            f"UPDATE {self.db_schema}.users SET {upd_datams} WHERE id = :id RETURNING *"
        )
        return await self.one_query(query, params.dict(exclude_unset=True) | {"id": id})

    async def get_row_count(self) -> int:
        return await self.get_value(f"SELECT count(0) FROM {self.db_schema}.users")
