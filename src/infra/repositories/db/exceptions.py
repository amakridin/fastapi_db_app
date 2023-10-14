from src.core.exceptions import DomainException


class EntityAlreadyExistsException(DomainException):
    pass


class EntityNotFoundException(DomainException):
    pass
