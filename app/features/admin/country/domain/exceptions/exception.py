from app.core.exceptions.domain import (
    DomainException,
    NotFoundException,
    AlreadyExistsException,
)


class CountryNotFoundException(NotFoundException):
    
    def __init__(self, entity: str, key: str):
        message = f"{entity} with {key} not found."
        self.message = message
        super().__init__(message)
    
class CountryAlreadyExistsException(AlreadyExistsException):
    
    def __init__(self, entity: str, key: str):
        message = f"{entity} with {key} already exists."
        self.message = message
        super().__init__(message)    
