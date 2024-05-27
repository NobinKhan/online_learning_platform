from asyncpg import UniqueViolationError

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import ORJSONResponse


router = APIRouter(
    prefix="/api/v1",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


