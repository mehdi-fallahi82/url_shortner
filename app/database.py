from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

db_name = "url_shortner_db"
db_user = "postgres"
db_pass = "123456"
db_port = "5432"
db_host = "db"

data_base_url = (
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
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