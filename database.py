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
#some comments on the database connection and collection setup
#1. The code imports necessary libraries and loads environment variables from a .env file using the `load_dotenv()` function. This allows for secure storage of sensitive information like database connection strings.
#2. The `MONGO_DETAILS` variable retrieves the MongoDB connection string from the environment