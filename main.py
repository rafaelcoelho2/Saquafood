from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database

app = FastAPI()
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

class PedidoSchema(BaseModel):
    cliente_nome: str
    itens: str
    pagamento: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    itens = db.query(models.Produto).all()
    return templates.TemplateResponse(request=request, name="index.html", context={"produtos": itens})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, db: Session = Depends(get_db)):
    itens = db.query(models.Produto).all()
    return templates.TemplateResponse(request=request, name="admin.html", context={"produtos": itens})

@app.get("/cozinha", response_class=HTMLResponse)
async def ver_cozinha(request: Request, db: Session = Depends(get_db)):
    fila = db.query(models.PedidoFila).filter(models.PedidoFila.status != "Pronto").order_by(models.PedidoFila.prioridade.asc(), models.PedidoFila.hora.asc()).all()
    return templates.TemplateResponse(request=request, name="cozinha.html", context={"pedidos": fila})

@app.post("/api/pedido")
async def pedido_site(dados: PedidoSchema, db: Session = Depends(get_db)):
    novo = models.PedidoFila(cliente="Online", cliente_nome=dados.cliente_nome, itens=dados.itens, pagamento=dados.pagamento, origem="Site", prioridade=2)
    db.add(novo)
    db.commit()
    return {"status": "ok"}

@app.post("/pedir/presencial")
async def pedido_mesa(cliente: str = Form(...), cliente_nome: str = Form(...), itens: str = Form(...), pagamento: str = Form(...), db: Session = Depends(get_db)):
    novo = models.PedidoFila(cliente=cliente, cliente_nome=cliente_nome, itens=itens, pagamento=pagamento, origem="Mesa", prioridade=1)
    db.add(novo)
    db.commit()
    return RedirectResponse(url="/cozinha", status_code=303)

@app.post("/admin/salvar")
async def salvar_prod(id: str = Form(None), nome: str = Form(...), preco: float = Form(...), descricao: str = Form(...), categoria: str = Form(...), imagem_url: str = Form(None), db: Session = Depends(get_db)):
    if id:
        p = db.query(models.Produto).filter(models.Produto.id == int(id)).first()
        p.nome, p.preco, p.descricao, p.categoria, p.imagem_url = nome, preco, descricao, categoria, imagem_url
    else:
        novo = models.Produto(nome=nome, preco=preco, descricao=descricao, categoria=categoria, imagem_url=imagem_url)
        db.add(novo)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/excluir/{id}")
async def excluir(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Produto).filter(models.Produto.id == id).first()
    if p:
        db.delete(p)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)
