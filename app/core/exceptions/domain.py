class DomainException(Exception):
    """Base class for domain exceptions."""
    pass

class NotFoundException(DomainException):
    """Exception raised when an entity is not found."""
    pass

class AlreadyExistsException(DomainException):
    """Exception raised when an entity already exists."""
    pass