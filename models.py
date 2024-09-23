from sqlalchemy import Column, Integer, Float, Date
from database import Base

# Modelo de datos para la tabla 'appl'
class StockData(Base):
    __tablename__ = 'appl'  # Nombre de nuestra tabla

    date = Column(Date, primary_key=True, index=True) # Index para búsquedas rápidas
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

# Podemos crear modelos adicionales para otras tablas...