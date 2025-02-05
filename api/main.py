import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from api.controllers import journal_router

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(journal_router)