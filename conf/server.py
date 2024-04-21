import time
import random
import string

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from sqladmin import Admin

from loguru import logger

from conf.database import async_engine
from app.admin.admin import UserAdmin, CourseAdmin


# Async Database Configuration
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    # await init_db()
    yield
    print("server is shutting down")


# main app
app = FastAPI(
    title="Online Learning Platform",
    description="Online Learning Platform API",
    version="0.1.0",
    lifespan=lifespan,
)
admin = Admin(app, async_engine)

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

admin.add_view(UserAdmin)
admin.add_view(CourseAdmin)
# routers definition
# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(movie.router)


# main root url
@app.get("/")
async def root():
    return {"message": "Hello OLP!"}
