from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    descricao = Column(String)
    categoria = Column(String)
    imagem_url = Column(String)

class PedidoFila(Base):
    __tablename__ = "pedidos_fila"
    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String)      # Ex: "Mesa 05" ou "Online"
    cliente_nome = Column(String) # Nome da pessoa
    itens = Column(String)
    pagamento = Column(String)    # Pix, Cartão, Dinheiro
    origem = Column(String)       # Mesa ou Site
    prioridade = Column(Integer)  # 1: Mesa, 2: Site
    status = Column(String, default="Pendente")
    hora = Column(DateTime, default=datetime.datetime.now)
