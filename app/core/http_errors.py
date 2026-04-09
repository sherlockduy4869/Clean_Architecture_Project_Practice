from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions.repository import (
    RepositoryException,
    ConnectionFailure,
    TransactionFailure,
    UniqueConstraintFailure,
)

from app.core.exceptions.domain import (
    DomainException,
    NotFoundException,
    AlreadyExistsException,
)



def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RepositoryException)
    async def handle_repository_exception(
        request: Request, exception: RepositoryException
    ):
        if isinstance(exception, ConnectionFailure):
            code = "DB_CONNECTION_FAILURE"
        elif isinstance(exception, TransactionFailure):
            code = "DB_TRANSACTION_FAILURE"
        elif isinstance(exception, UniqueConstraintFailure):
            code = "DB_UNIQUE_CONSTRAINT_FAILURE"
        else:
            code = "DB_UNKNOWN_FAILURE"

        return JSONResponse(
            status_code=503,
            content={
                "code": code,
                "message": "A database error occurred. Please try again later.",
            },
        )

    @app.exception_handler(DomainException)
    async def handle_domain_exception(
        request: Request, exception: DomainException
    ):
        if isinstance(exception, NotFoundException):
            code = "NOT_FOUND"
            message = getattr(exception, "message", "The requested resource was not found.")
        elif isinstance(exception, AlreadyExistsException):
            code = "ALREADY_EXISTS"
            message = getattr(exception, "message", "The resource already exists.")
        else:
            code = "DOMAIN_UNKNOWN_FAILURE"
            message = getattr(exception, "message", "Domain service temporarily unavailable. Please try again later.")

        return JSONResponse(
            status_code= 400,
            content={
                "code": code,
                "message": message,
            },
        )
