from azure.identity import DefaultAzureCredential
from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from datetime import datetime
from typing import Any, Dict, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from api.repositories.interface_respository import DatabaseInterface
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")

if not COSMOS_ENDPOINT:
    raise ValueError("COSMOS_ENDPOINT environment variable is missing")
if not COSMOS_DATABASE_NAME:
    raise ValueError("COSMOS_DATABASE_NAME environment variable is missing")

class CosmosDB(DatabaseInterface):
    def __init__(self):
        self.database_name = COSMOS_DATABASE_NAME
        self.client = None
        
    async def __aenter__(self):
        logger.info("Initializing CosmosClient.")
        self.client = CosmosClient(
            url=COSMOS_ENDPOINT,
            credential=DefaultAzureCredential()
        )
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        logger.info("Closing CosmosClient.")
        await self.client.close()

    @asynccontextmanager
    async def _get_container(self, container_name: str):
        if self.client is None:
            logger.error("CosmosClient not initialized when accessing container %s.", container_name)
            raise ValueError("CosmosClient not initialized. Please use 'async with CosmosDB() as db:'")
        database = self.client.get_database_client(self.database_name)
        container = database.get_container_client(container_name)
        logger.debug("Accessing container: %s", container_name)
        yield container
        
    def _serialize_date(self, dt):
        return dt.isoformat() if isinstance(dt, datetime) else dt
        

    async def create_entry(self, entry_data: Dict[str, Any]) -> None:
        logger.info("Creating a new entry.")
        async with self._get_container("test_entries") as container:
            if "created_at" in entry_data:
                entry_data["created_at"] = self._serialize_date(entry_data["created_at"])
            if "updated_at" in entry_data:
                entry_data["updated_at"] = self._serialize_date(entry_data["updated_at"])
            await container.create_item(body=entry_data)
            logger.debug("Entry created.")

    async def get_entries(self) -> List[Dict[str, Any]]:
        logger.debug("Getting all entries.")
        async with self._get_container("test_entries") as container:
            query = "SELECT * FROM c"
            items = [item async for item in container.query_items(query=query)]
            logger.debug("Retrieved %d entries.", len(items))
            return items
    
    async def delete_all_entries(self) -> None:
        logger.info("Deleting all entries.")
        async with self._get_container("test_entries") as container:
            query = "SELECT * FROM c"
            async for item in container.query_items(query=query):
                await container.delete_item(item=item['id'], partition_key=item['id'])
                logger.debug("Deleted entry id: %s", item['id'])
                
    async def delete_entry(self, entry_id: str) -> None:
        logger.info("Deleting entry with id: %s", entry_id)
        async with self._get_container("test_entries") as container:
            await container.delete_item(item=entry_id, partition_key=entry_id)
            logger.debug("Deleted entry with id: %s", entry_id)
    
    async def get_entry(self, entry_id: str) -> Dict[str, Any]:
        logger.info("Getting entry with id: %s", entry_id)
        async with self._get_container("test_entries") as container:
            try:
                item = await container.read_item(item=entry_id, partition_key=entry_id)
                logger.debug("Retrieved entry with id: %s", entry_id)
                return item
            except CosmosResourceNotFoundError:
                logger.error("Entry with id %s not found.", entry_id)
                raise
    
    async def update_entry(self, entry_data: Dict[str, Any]) -> None:
        entry_id = entry_data.get("id")
        if not entry_id:
            raise ValueError("entry_data must contain 'id' key for update.")
        if "updated_at" in entry_data:
            entry_data["updated_at"] = self._serialize_date(entry_data["updated_at"])
        else:
            entry_data["updated_at"] = self._serialize_date(datetime.utcnow())
        logger.info("Updating entry with id: %s", entry_id)
        async with self._get_container("test_entries") as container:
            await container.replace_item(item=entry_id, body=entry_data)
            logger.debug("Updated entry with id: %s", entry_id)