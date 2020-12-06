from sqlalchemy import Column, Date, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'
    yahoo_id = Column(String)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)
