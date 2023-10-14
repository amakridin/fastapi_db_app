from src.core.model import Page
from src.infra.repositories.db.db_user_repository import DBUserRepository


class UserManager:
    def __init__(self, db_user_repository: DBUserRepository):
        self.db_user_repository = db_user_repository

    async def get_paged_users(self, limit: int, offset: int) -> Page:
        total = await self.db_user_repository.get_row_count()
        return Page(
            items=await self.db_user_repository.get_many(limit, offset),
            offset=offset,
            limit=limit,
            total=total,
        )
