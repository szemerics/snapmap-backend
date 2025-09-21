from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from dotenv import load_dotenv
import os

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')
database = os.getenv('DATABASE_NAME')

client = AsyncIOMotorClient(mongodb_uri, tlsAllowInvalidCertificates=True)
engine = AIOEngine(client=client, database=database)