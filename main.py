from fastapi import FastAPI, HTTPException
from psycopg import IntegrityError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models import Categoria

app = FastAPI()

class CategoriaCreate(BaseModel):
    name: str

@app.get("/health")
def health_check():
    return {"status": "API Funcionando..."}




@app.post("/categorias")
def criar_categoria(dados: CategoriaCreate):
    with Session(engine) as session:
        try:
            categoria = Categoria(name=dados.name)
            session.add(categoria)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="Categoria já existe.")
        
        session.refresh(categoria)
        return {"id": categoria.id, "name": categoria.name}


@app.get("/categorias")
def listar_categorias():
    with Session(engine) as session:
        categorias = session.scalars(select(Categoria)).all()
        return [{"id": categoria.id, "name": categoria.name} for categoria in categorias]