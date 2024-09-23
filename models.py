from sqlalchemy import Column, Integer, Float, Date
from database import Base


class StockData(Base):
    __tablename__ = 'appl'  # Nombre de tu tabla

    date = Column(Date, primary_key=True, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
