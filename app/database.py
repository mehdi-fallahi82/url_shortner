from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

data_base_url = (
    f"postgresql+psycopg2://postgres:123456@127.0.0.1:5432/url_shortner_db"
)
engine = create_engine(data_base_url)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()