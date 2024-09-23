from sqlalchemy import Column, Integer, Float, Date
from database import Base

class StockData(Base):
    __tablename__ = 'stock_data'  # Nombre de tu tabla

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
