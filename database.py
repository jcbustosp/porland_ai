import os
import dotenv

from toolfront import Database
from trino.auth import OAuth2Authentication

dotenv.load_dotenv(override=True)

db = Database.from_trino(
    user=os.getenv("USER"),
    host=os.getenv("TRINO_HOST"),
    port=os.getenv("TRINO_PORT"),
    database=os.getenv("TRINO_CATALOG"),
    schema=os.getenv("TRINO_SCHEMA"),
    match_schema=f"^{os.getenv('TRINO_SCHEMA')}$",
    auth=OAuth2Authentication(),
    http_scheme="https",
)