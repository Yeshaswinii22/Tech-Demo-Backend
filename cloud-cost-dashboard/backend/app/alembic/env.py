import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.alembic import context
from app.database import Base  # Import your models

load_dotenv()
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
