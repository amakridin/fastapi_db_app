from aiopg.sa import create_engine, Engine

from src.infra.repositories.db.db_base import DBBaseRepository


class Resources:
    def __init__(self, engine: Engine):
        self.engine = engine

    @classmethod
    async def _create_engine(cls, config):
        return await create_engine(
            dsn=config.dsn,
            minsize=config.pg_min_pool_size,
            maxsize=config.pg_max_pool_size,
        )

    @classmethod
    async def init_resources(cls, config):
        return cls(engine=await cls._create_engine(config))
