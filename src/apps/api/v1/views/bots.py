from fastapi import APIRouter, Depends

from src.apps.api.dependencies import bot_manager_dependency
from src.core.bots import BotManager
from src.core.model import CreateBotParams, SuccessResult
from src.infra.repositories.db.model import Bot

router = APIRouter(
    prefix="/bots",
    tags=["bots"],
)


@router.post("", response_model=Bot, description="create bot")
async def create_bot(
    params: CreateBotParams,
    bot_manager: BotManager = Depends(bot_manager_dependency),
) -> Bot:
    return await bot_manager.create_bot(params)


@router.delete("/{token}", response_model=str)
async def delete_bot(
    token: str,
    repo: BotManager = Depends(bot_manager_dependency),
) -> SuccessResult():
    await repo.delete_bot_by_token(token)
