import time
import random
import string
from os import environ

from loguru import logger
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from edgy import Database, Registry


# env configuration
load_dotenv(".env")

# Database configuration
database = Database(
    url=f"{environ.get("DATABASE_SCHEME")}://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}:{environ.get('POSTGRES_PORT')}/{environ.get('POSTGRES_DB')}",
)
db_models = Registry(database=database)

# main app
app = FastAPI(
    title="Online Learning Platform",
    description="Online Learning Platform API",
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)


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
# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(movie.router)


# main root url
@app.get("/")
async def root():
    return {"message": "Hello OLP!"}
