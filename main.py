from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

engine = create_engine("sqlite:///./saquafood.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    imagem = Column(String)

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/cardapio")
def listar(db: Session = Depends(get_db)):
    return db.query(Produto).all()

@app.get("/adicionar")
def add(nome: str, preco: float, imagem: str = None, db: Session = Depends(get_db)):
    novo = Produto(nome=nome, preco=preco, imagem=imagem or "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500")
    db.add(novo)
    db.commit()
    return {"msg": "Sucesso"}

@app.get("/editar_prod")
def editar(id: int, nome: str, preco: float, imagem: str, db: Session = Depends(get_db)):
    item = db.query(Produto).filter(Produto.id == id).first()
    if item:
        item.nome = nome
        item.preco = preco
        item.imagem = imagem
        db.commit()
        return {"msg": "Atualizado"}
    return {"error": "Não encontrado"}

@app.get("/deletar/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    item = db.query(Produto).filter(Produto.id == id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"msg": "Removido"}
