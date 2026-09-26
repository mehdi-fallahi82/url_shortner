from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

data_base_url = "postgresql://postgres:meh1382di@localhost:5432/url_shortner_db"


engine = create_engine(data_base_url)

Base = declarative_base()

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()