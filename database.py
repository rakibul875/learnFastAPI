import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import certifi


load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(
    MONGO_DETAILS,
    tlsCAFile=certifi.where()
)

database = client["my_fastapi_db"]
users_collection = database["users"]