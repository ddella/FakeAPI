from pydantic import BaseSettings
from logger import logging
import os

# Set environment variable (for testing ONLY)
# os.environ['FAKEAPI_ENV'] = './.env'

# Get environment variable for main configuration file
ENV = os.getenv('FAKEAPI_ENV')
# If ENV doesn't exist, set it to local file
if ENV is None:
    ENV = './.env'
    logging.info(f'Unknown environnement variable, using local file "{ENV}"')

class Settings(BaseSettings):
    MONGO_DB_URI: str
    MONGO_INITDB_DATABASE: str
    MONGO_INITDB_COLLECTION: str
    MONGO_DB_TIMEOUT: int

    # Interface to listen on
    FAKEAPI_HOST: str
    # TCP port
    FAKEAPI_PORT: int
    # If you want to use HTTP instead of HTTPS, just comment both lines
    FAKEAPI_PKEY: str
    FAKEAPI_CRT: str

    class Config:
        env_file = ENV


settings = Settings()
