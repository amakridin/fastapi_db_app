from src.core.exceptions import BotAlreadyExistsException
from src.core.model import CreateBotSchema, CreateBotParams, Page
from src.infra.repositories.db.db_bot_repository import DBBotRepository
from src.infra.repositories.db.exceptions import EntityNotFoundException
from src.infra.repositories.db.model import Bot, DBCreateBotParams


class BotManager:
    def __init__(
        self,
        db_bot_repository: DBBotRepository,
        schema_prefix: str,
    ):
        self.db_bot_repository = db_bot_repository
        self.schema_prefix = schema_prefix

    async def create_bot(self, params: CreateBotParams) -> Bot:
        try:
            if await self.db_bot_repository.get_by_bot_id(params.bot_id):
                raise BotAlreadyExistsException
        except EntityNotFoundException:
            pass

        bot: Bot = await self.db_bot_repository.create(
            DBCreateBotParams(**params.dict())
        )
        bot_schema_params = CreateBotSchema(
            recreate=True,
            db_schema=self.get_bot_schema(bot.bot_id),
        )
        with open("src/infra/repositories/db/migrator/bot_tables.sql") as sql:
            await self.db_bot_repository.execute_query(
                sql.read().format(**bot_schema_params.dict())
            )
        return bot

    async def delete_bot_by_bot_id(self, bot_id: str) -> None:
        bot = await self.db_bot_repository.delete_by_bot_id(bot_id)
        await self._drop_bot_schema(schema=self.get_bot_schema(bot.bot_id))

    async def get_paged_bots(self, limit: int, offset: int) -> Page:
        total = await self.db_bot_repository.get_row_count()
        return Page(
            items=await self.db_bot_repository.get_many(limit, offset),
            offset=offset,
            limit=limit,
            total=total,
        )

    def get_bot_schema(self, bot_id: str):
        return f"{self.schema_prefix}{bot_id}"

    async def _drop_bot_schema(self, schema: str) -> None:
        query = 'DROP SCHEMA IF EXISTS ":schema" CASCADE'
        await self.db_bot_repository.execute_query(query, {"schema": schema})
