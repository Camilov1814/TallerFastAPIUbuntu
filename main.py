from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from pydantic import BaseModel
from typing import List, Annotated, Optional
from datetime import date
import models 
from database import SessionLocal, engine
from sqlalchemy.orm import Session



app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Crear las tablas en la base de datos

# Pydantic schema para la respuesta
class StockData(BaseModel):
    close: float
    low: float
    open: float
    date: date  
    high: float
    adj_close: float
    volume: int

    class Config:
        # orm_mode = True  # Para convertir el modelo SQLAlchemy a Pydantic
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
#############################################################################################
@app.get("/stocks/")
async def get_stocks(
    db: db_dependency,
    page: int = 1,
    limit: int = 100,
    date_from: Optional[date] = Query(None, description="Filtrar desde esta fecha"),
    date_to: Optional[date] = Query(None, description="Filtrar hasta esta fecha")
):
    
    # Validar los parámetros de paginación 400 - Bad Request
    if page < 1:
        raise HTTPException(status_code=400, detail="El número de página debe ser mayor o igual a 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="El límite debe ser mayor o igual a 1")

    # Iniciar la consulta
    query = db.query(models.StockData)

    # Filtrar por fechas si se proporcionan
    if date_from:
        query = query.filter(models.StockData.date >= date_from)
    if date_to:
        query = query.filter(models.StockData.date <= date_to)

    total_records = query.count()
    max_pages = (total_records + limit - 1) // limit  # Redondear hacia arriba
    # Verificar si la página solicitada está fuera de rango
    if page > max_pages:
        raise HTTPException(
            status_code=400, 
            detail=f"La página solicitada {page} está fuera del rango. Solo hay {max_pages} páginas disponibles."
        )

    page = (page - 1) * limit

    # Paginación
    stocks = query.offset(page).limit(limit).all()

    if not stocks:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los filtros proporcionados")

    return stocks



# Endpoint POST para crear datos de acciones
#############################################################################################
@app.post("/stocks/")
async def create_stock_data(stock_data: list[StockData]):
    db = SessionLocal()
    created_count = 0

    for stock in stock_data:
        # Verificar si ya existe una acción con la misma fecha
        existing_stock = db.query(models.StockData).filter(models.StockData.date == stock.date).first()
        if existing_stock:
            raise HTTPException(
                status_code=409,  # Código de estado HTTP 409 Conflict
                detail=f"La acción con la fecha {stock.date} ya existe en la base de datos Se agregaron {created_count} elementos a la base de datos.",
            )

        # Creación de un objeto de la clase StockData
        stock_entry = models.StockData(
            close=stock.close,
            low=stock.low,
            open=stock.open,
            date=stock.date,
            high=stock.high,
            adj_close=stock.adj_close,
            volume=stock.volume
        )
        try:
            db.add(stock_entry)
            db.commit()
            created_count += 1
        except IntegrityError:
            db.rollback()  # Deshacer cambios en caso de error
            continue

    total_count = db.query(models.StockData).count()  # Total de registros en la base de datos
    db.close()

    return JSONResponse(content={
        "created_count": created_count,
        "total_count": total_count
    })
