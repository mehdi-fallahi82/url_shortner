from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column
from app.database import Base

class url_items(Base):
    __tablename__ = 'urls'

    id = Column(Integer, index=True ,primary_key=True)
    original_url = Column(String , nullable=False)
    short_code = Column(String , unique=True ,index=True ,nullable=False)
    creation_at = Column(DateTime, default=datetime.now)
    clicks = Column(Integer, default=0)

