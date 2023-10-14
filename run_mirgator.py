import asyncio

from resources import Resources
from src.apps.api.v1.app import Settings


async def run() -> None:
    """
    This block run sql migrations for ddl or dml operations only for base tables
    Bot tables create during creating of new bot
    """
    resources = await Resources.init_resources(Settings())
    with open("src/infra/repositories/db/migrator/base_tables.sql") as f:
        async with resources.engine.acquire() as con:
            await con.execute(f.read())


if __name__ == "__main__":
    asyncio.run(run())
