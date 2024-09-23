from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Annotated, Optional
from datetime import date
import models 
from database import SessionLocal, engine
from sqlalchemy.orm import Session



app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Crear las tablas en la base de datos

# Pydantic schema para la respuesta
class StockItem(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    class Config:
        # orm_mode = True  # Para convertir el modelo SQLAlchemy a Pydantic
        from_attributes = True

# Pydantic schema para la petición
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        # orm_mode = True
        from_attributes = True

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# Endpoint GET con filtros y paginación
@app.get("/stocks/")
async def get_stocks(
    db: db_dependency,
    page: int = 1,
    limit: int = 100,
    date_from: Optional[date] = Query(None, description="Filtrar desde esta fecha"),
    date_to: Optional[date] = Query(None, description="Filtrar hasta esta fecha")
):
    # Iniciar la consulta
    query = db.query(models.StockData)

    # Filtrar por fechas si se proporcionan
    if date_from:
        query = query.filter(models.StockData.date >= date_from)
    if date_to:
        query = query.filter(models.StockData.date <= date_to)

    page = page * limit - limit

    # Paginación
    stocks = query.offset(page).limit(limit).all()

    return stocks
