import asyncio
import asyncpg
from loguru import logger


class PostgresPool:
    """A context manager for handling asyncpg connection pools."""

    def __init__(self, dsn):
        self.dsn = dsn
        self.min_size = 2
        self.max_size = 10
        self.pool: asyncpg.Pool | None = None

    async def __aenter__(self) -> asyncpg.Pool:
        logger.info("Creating database connection pool.")

        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
        )
        if self.pool is None:
            raise RuntimeError("Failed to create database connection pool.")

        logger.info("Created database connection pool.")
        return self.pool

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.pool is not None:
            logger.info("Closing database connection pool.")
            await asyncio.wait_for(self.pool.close(), timeout=10)
            logger.info("Database connection pool closed.")
