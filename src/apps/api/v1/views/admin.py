from fastapi import APIRouter, Depends, Query

from src.apps.api.dependencies import (
    db_bot_repo_dependency,
    bot_manager_dependency,
    validate_api_key,
)
from src.core.bots import BotManager
from src.core.model import Page, SuccessResult
from src.infra.repositories.db.db_bot_repository import DBBotRepository
from src.infra.repositories.db.model import Bot

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(validate_api_key)],
)


@router.get("/bots/paged", response_model=Page, description="get bots paged")
async def get_bots_paged(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=100),
    bot_manager: BotManager = Depends(bot_manager_dependency),
) -> Page:
    return await bot_manager.get_paged_bots(limit, offset)


@router.get("/bot/{entity_id}", response_model=Bot, description="get bot by bot_id")
async def get_bot_by_bot_id(
    entity_id: str,
    repo: DBBotRepository = Depends(db_bot_repo_dependency),
) -> Bot:
    return await repo.get_by_bot_id(entity_id)


@router.delete("/bot/{entity_id}", response_model=SuccessResult)
async def delete_bot(
    entity_id: str,
    repo: BotManager = Depends(bot_manager_dependency),
) -> SuccessResult:
    await repo.delete_bot_by_bot_id(entity_id)
    return SuccessResult()
