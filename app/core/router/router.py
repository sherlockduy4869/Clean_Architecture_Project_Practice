from fastapi import APIRouter

def get_versioned_router(version: str):
    return APIRouter(prefix=f"/{version}")