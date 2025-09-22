from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from database import SessionLocal, engine
from models import Livro as LivroModel
import models

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API da Biblioteca com Banco de Dados")

# Pydantic (schemas)
class LivroCreate(BaseModel):
    titulo: str
    autor: str

class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    alugado: bool

    class Config:
        orm_mode = True

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints

@app.post("/livros", response_model=LivroResponse)
def adicionar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    db_livro = LivroModel(titulo=livro.titulo, autor=livro.autor)
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

@app.get("/livros/disponiveis", response_model=List[LivroResponse])
def listar_disponiveis(db: Session = Depends(get_db)):
    return db.query(LivroModel).filter(LivroModel.alugado == False).all()

@app.get("/livros/alugados", response_model=List[LivroResponse])
def listar_alugados(db: Session = Depends(get_db)):
    return db.query(LivroModel).filter(LivroModel.alugado == True).all()

@app.post("/livros/alugar/{livro_id}")
def alugar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroModel).filter(LivroModel.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    if livro.alugado:
        raise HTTPException(status_code=400, detail="Livro já está alugado")
    livro.alugado = True
    db.commit()
    return {"mensagem": f"Livro '{livro.titulo}' alugado com sucesso"}

@app.post("/livros/devolver/{livro_id}")
def devolver_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(LivroModel).filter(LivroModel.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    if not livro.alugado:
        raise HTTPException(status_code=400, detail="Livro não está alugado")
    livro.alugado = False
    db.commit()
    return {"mensagem": f"Livro '{livro.titulo}' devolvido com sucesso"}
