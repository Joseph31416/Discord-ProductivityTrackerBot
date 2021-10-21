import os
from dotenv import load_dotenv

load_dotenv()


DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
TOKEN = os.environ.get("TOKEN")
TEST_TOKEN = os.environ.get("TEST_TOKEN")
TEXT_CHANNEL = os.environ.get("TEXT_CHANNEL")
TEST_TEXT_CHANNEL = os.environ.get("TEST_TEXT_CHANNEL")
BLACKLIST = os.environ.get("BLACKLIST")
BLACKLIST_RESP = os.environ.get("BLACKLIST_RESP")
