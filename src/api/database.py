from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api import config

engine = create_engine(url=str(config.cfg.get("DATABASE_URL", "")))
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
