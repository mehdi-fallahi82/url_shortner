from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column
from app.database import Base

class URLItem(Base):
    __tablename__ = 'url_items'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)



