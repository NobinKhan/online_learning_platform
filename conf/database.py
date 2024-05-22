from asyncpg import connect as postgres_connect
from asyncpg.exceptions import InvalidCatalogNameError, InvalidPasswordError
from loguru import logger

from conf.settings import settings


class Postgresql:
    async def db_conn(self):
        try:
            logger.info("connecting to database")
            conn = await postgres_connect(dsn=await settings.postgres_url())
            db_name = await conn.fetchval("SELECT current_database()")
            logger.info(f"database {db_name} connected")
            return conn
        except InvalidCatalogNameError:
            logger.error(
                f"database {settings.POSTGRES_DB.get_secret_value()} not found"
            )
        except ConnectionRefusedError:
            logger.error(
                "database connection refused, please check the database settings"
            )
        except InvalidPasswordError:
            logger.error("invalid credentials, please check the database settings")
