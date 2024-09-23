from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos PostgreSQL
psw = 'jose'
DATABASE_URL = f"postgresql://postgres:{psw}@localhost:5432/AppleStocks"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 
