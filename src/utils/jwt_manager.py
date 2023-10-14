from datetime import datetime, timedelta, timezone
from typing import Any
from hashlib import sha256

import jwt
from jwt.exceptions import ExpiredSignatureError

from src.core.exceptions import DomainException


class JWTDecodeException(DomainException):
    pass


class JWTExpiredException(DomainException):
    pass


class JWTManager:
    def __init__(self, secret_key: str, ttl: int, **kwargs):
        """
        В **kwargs ожидаем параметры, которые определяют класс как отдельная сущность
        """
        self.secret_key = secret_key
        self.ttl = ttl
        self.params = kwargs

    @property
    def token_expiration(self):
        return datetime.now(tz=timezone.utc) + timedelta(seconds=self.ttl)

    def encode(self, **kwargs) -> str:
        """
        В **kwargs ожидаем параметры токена, для которых формируется токен в рамках класса
        Пример: email (str) - email пользователя
        """
        payload = dict()
        payload.update(self.params)
        payload.update(**kwargs)
        if self.ttl > 0:
            payload.update(exp=self.token_expiration)
        return jwt.encode(
            key=self.secret_key,
            payload=payload,
        )

    def decode(self, payload: str) -> dict[str, Any]:
        try:
            return jwt.decode(jwt=payload, key=self.secret_key, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise JWTExpiredException
        except Exception as ex:
            raise JWTDecodeException from ex

    def get_token_hash(self, token: str):
        return sha256(token.encode()).hexdigest()
