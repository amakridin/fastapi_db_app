from fastapi import APIRouter, Depends, Query, Request

from src.apps.api.dependencies import (
    db_user_repo_dependency,
    user_manager_dependency,
    validate_api_key,
)
from src.core.model import Page
from src.core.users import UserManager
from src.infra.repositories.db.db_user_repository import DBUserRepository
from src.infra.repositories.db.model import DBCreateUserParams, UpdateUserParams, User

router = APIRouter(
    prefix="/bot/{bot_id}/user",
    tags=["user"],
    dependencies=[Depends(validate_api_key)],
)


@router.get("/paged", response_model=Page, description="get users paged")
async def get_users_paged(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=100),
    user_manager: UserManager = Depends(user_manager_dependency),
) -> Page:
    return await user_manager.get_paged_users(limit, offset)


@router.get("/{entity_id}", response_model=User, description="get user by id")
async def get_user_by_id(
    entity_id: int,
    repo: DBUserRepository = Depends(db_user_repo_dependency),
) -> User:
    return await repo.get_one(entity_id)


@router.post("", response_model=User, description="create user")
async def create_user(
    params: DBCreateUserParams,
    repo: DBUserRepository = Depends(db_user_repo_dependency),
) -> User:
    return await repo.create(params)


@router.put("/{entity_id}", response_model=User, description="update user")
async def update_user(
    entity_id: int,
    params: UpdateUserParams,
    repo: DBUserRepository = Depends(db_user_repo_dependency),
) -> User:
    return await repo.update(entity_id, params)


@router.delete("/{entity_id}", response_model=User)
async def delete_user(
    entity_id: int,
    repo: DBUserRepository = Depends(db_user_repo_dependency),
) -> User:
    return await repo.delete(entity_id)
