from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "forsitDB"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
