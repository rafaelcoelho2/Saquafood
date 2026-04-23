from sqlalchemy import Column, Integer, String, Float
from database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    imagem = Column(String)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    endereco = Column(String)

class Bairro(Base):
    __tablename__ = "bairros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    taxa = Column(Float)
