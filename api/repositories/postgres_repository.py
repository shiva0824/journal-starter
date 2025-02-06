import os
import uuid
import logging
import asyncpg
from datetime import datetime
from typing import Any, Dict, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from api.repositories.interface_respository import DatabaseInterface

load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")

class PostgresDB(DatabaseInterface):
    async def __aenter__(self):
        logger.info("Creating Postgres connection pool.")
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger.info("Closing Postgres connection pool.")
        await self.pool.close()

    async def create_entry(self, entry_data: Dict[str, Any]) -> None:
        logger.info("Creating a new entry in Postgres.")
        async with self.pool.acquire() as conn:
            query = """
            INSERT INTO entries (id, data, created_at, updated_at)
            VALUES ($1, $2, $3, $4)
            """
            entry_id = entry_data.get("id") or str(uuid.uuid4())
            await conn.execute(query, entry_id, entry_data, entry_data["created_at"], entry_data["updated_at"])
            logger.debug("Entry created with id: %s", entry_id)

    async def get_entries(self) -> List[Dict[str, Any]]:
        logger.debug("Getting all entries from Postgres.")
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM entries"
            rows = await conn.fetch(query)
            return [dict(row) for row in rows]

    async def get_entry(self, entry_id: str) -> Dict[str, Any]:
        logger.info("Getting entry with id: %s from Postgres", entry_id)
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM entries WHERE id = $1"
            row = await conn.fetchrow(query, entry_id)
            if row:
                return dict(row)
            logger.error("Entry with id %s not found in Postgres", entry_id)
            return None

    async def update_entry(self, entry_id: str, updated_data: Dict[str, Any]) -> None:
        logger.info("Updating entry with id: %s in Postgres", entry_id)
        async with self.pool.acquire() as conn:
            query = """
            UPDATE entries SET data = $2, updated_at = $3
            WHERE id = $1
            """
            await conn.execute(query, entry_id, updated_data, updated_data["updated_at"])
            logger.debug("Entry %s updated in Postgres", entry_id)

    async def delete_entry(self, entry_id: str) -> None:
        logger.info("Deleting entry with id %s from Postgres", entry_id)
        async with self.pool.acquire() as conn:
            query = "DELETE FROM entries WHERE id = $1"
            await conn.execute(query, entry_id)
            logger.debug("Entry %s deleted from Postgres", entry_id)

    async def delete_all_entries(self) -> None:
        logger.info("Deleting all entries in Postgres")
        async with self.pool.acquire() as conn:
            query = "DELETE FROM entries"
            await conn.execute(query)
            logger.debug("All entries deleted from Postgres")
