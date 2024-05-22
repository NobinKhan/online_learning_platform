import time
import random
import string

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination

from loguru import logger

from conf.database import Postgresql
from api.course import course


# Async Database Configuration
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db_conn = await Postgresql().db_conn()

        app.state = {"db_conn": db_conn}
        logger.info("Server is starting")

        yield
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    finally:
        if db_conn is not None:
            await app.state.get("db_conn").close()
        logger.info("Server is shutting down")


# main app
app = FastAPI(
    title="Online Learning Platform",
    description="Online Learning Platform API",
    version="0.1.0",
    lifespan=lifespan,
    redoc_url=None,
)
add_pagination(app)


# middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}",
    )

    return response


# routers definition
app.include_router(course.router)
# app.include_router(user.router)
# app.include_router(movie.router)


# main root url
@app.get("/")
async def root():
    return {"message": "Hello OLP!"}
