from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import StockData
from pydantic import BaseModel
from datetime import date

app = FastAPI()

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
        orm_mode = True  # Para convertir el modelo SQLAlchemy a Pydantic

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        orm_mode = True
# Endpoint GET con filtros y paginación
@app.get("/stocks/", response_model=List[StockItem])
def get_stocks(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = Query(None, description="Filtrar desde esta fecha"),
    date_to: Optional[date] = Query(None, description="Filtrar hasta esta fecha"),
    db: Session = Depends(get_db)
):
    # Iniciar la consulta
    query = db.query(StockData)

    # Filtrar por fechas si se proporcionan
    if date_from:
        query = query.filter(StockData.date >= date_from)
    if date_to:
        query = query.filter(StockData.date <= date_to)

    # Paginación
    stocks = query.offset(skip).limit(limit).all()

    return stocks

@app.get("/items/{item_id}")
def read_item(item_id: int, query: str = None):
    return {"item_id": item_id, "query": query}

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "description": item.description, "price": item.price}


