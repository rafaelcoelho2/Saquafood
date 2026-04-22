from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import models, database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
security = HTTPBasic()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "saqua123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso Negado")
    return credentials.username

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f: return f.read()

@app.get("/admin", response_class=HTMLResponse)
def admin(username: str = Depends(verificar_admin)):
    with open("templates/admin.html", "r", encoding="utf-8") as f: return f.read()

# --- ROTAS DE PRODUTOS ---
@app.get("/api/produtos")
def listar_p(db: Session = Depends(database.get_db)): return db.query(models.Produto).all()

@app.post("/api/admin/produtos")
def cadastrar_p(nome: str, preco: float, imagem: str, db: Session = Depends(database.get_db), u=Depends(verificar_admin)):
    novo = models.Produto(nome=nome, preco=preco, imagem=imagem)
    db.add(novo)
    db.commit()
    return {"s": "ok"}

# --- ROTAS DE CLIENTES ---
@app.get("/api/admin/clientes")
def listar_c(db: Session = Depends(database.get_db), u=Depends(verificar_admin)):
    return db.query(models.Cliente).all()

@app.post("/api/admin/clientes")
def cadastrar_c(nome: str, tel: str, end: str, db: Session = Depends(database.get_db), u=Depends(verificar_admin)):
    novo = models.Cliente(nome=nome, telefone=tel, endereco=end)
    db.add(novo)
    db.commit()
    return {"s": "ok"}

@app.delete("/api/admin/clientes/{c_id}")
def deletar_c(c_id: int, db: Session = Depends(database.get_db), u=Depends(verificar_admin)):
    c = db.query(models.Cliente).filter(models.Cliente.id == c_id).first()
    db.delete(c); db.commit()
    return {"s": "ok"}
