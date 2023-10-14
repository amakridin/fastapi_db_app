import re


class DomainException(Exception):
    def __init__(self, details=None):
        self.details = details

    def __str__(self):
        s = re.sub(r"Exception$", "", self.__class__.__name__)
        return "".join(["_" + c if c.isupper() else c.upper() for c in s]).lstrip("_")


class MissingApiKeyException(DomainException):
    pass


class InvalidApiKeyException(DomainException):
    pass


class MissingTokenException(DomainException):
    pass


class InvalidTokenException(DomainException):
    pass


class ExpiredTokenException(DomainException):
    pass


class BotAlreadyExistsException(DomainException):
    pass
