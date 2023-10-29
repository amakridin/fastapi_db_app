from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, constr
from pydantic.class_validators import root_validator


class User(BaseModel):
    id: int
    name: str
    locale: str


class DBCreateUserParams(BaseModel):
    name: str
    locale: str


class UpdateUserParams(BaseModel):
    name: Optional[str]
    locale: Optional[str]

    @root_validator
    def validate_all(cls, values):
        if not any(set(values.values())):
            keys = ", ".join([f"'{k}'" for k in values])
            raise Exception(f"Validation error. At least one of: {keys} must be set")
        return values


class Bot(BaseModel):
    bot_id: str
    date_created: datetime


class DBCreateBotParams(BaseModel):
    bot_id: constr(to_lower=True, strip_whitespace=True, regex="^[a-z0-9][a-z0-9-]*$")
