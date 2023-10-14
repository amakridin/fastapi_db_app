from pydantic import BaseModel, constr, Field


class SuccessResult(BaseModel):
    result: str = Field(default="Ok")


class Page(BaseModel):
    items: list
    offset: int
    limit: int
    total: int


class CreateBotSchema(BaseModel):
    recreate: bool
    db_schema: str


class CreateBotParams(BaseModel):
    bot_id: constr(to_lower=True, strip_whitespace=True, regex="^[a-z0-9][a-z0-9-]*$")


class JwtTokenModel(BaseModel):
    bot_id: str
