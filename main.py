from fastapi import FastAPI
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
        categoria = Categoria(name=dados.name)
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return {"id": categoria.id, "name": categoria.name}


@app.get("/categorias")
def listar_categorias():
    with Session(engine) as session:
        categorias = session.scalars(select(Categoria)).all()
        return [{"id": categoria.id, "name": categoria.name} for categoria in categorias]