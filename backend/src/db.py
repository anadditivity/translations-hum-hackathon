from config import DB_USER, DB_PASSWORD 
from sqlalchemy import create_engine

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@db/translation_db:5432"
engine = create_engine(f"{DATABASE_URL}", echo=True)
con = engine.connect()


