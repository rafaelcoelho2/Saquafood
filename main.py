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

def ver_admin(cred: HTTPBasicCredentials = Depends(security)):
    if cred.username != "admin" or cred.password != "saqua123":
        raise HTTPException(status_code=401)
    return cred.username

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f: return f.read()

@app.get("/admin", response_class=HTMLResponse)
def admin(u=Depends(ver_admin)):
    with open("templates/admin.html", "r", encoding="utf-8") as f: return f.read()

@app.get("/api/produtos")
def list_p(db: Session = Depends(database.get_db)): return db.query(models.Produto).all()

@app.get("/api/bairros")
def list_b(db: Session = Depends(database.get_db)): return db.query(models.Bairro).all()

@app.post("/api/admin/produtos")
def add_p(nome:str, preco:float, imagem:str, db:Session=Depends(database.get_db), u=Depends(ver_admin)):
    db.add(models.Produto(nome=nome, preco=preco, imagem=imagem)); db.commit(); return {"s":"ok"}

@app.post("/api/admin/bairros")
def add_b(nome:str, taxa:float, db:Session=Depends(database.get_db), u=Depends(ver_admin)):
    db.add(models.Bairro(nome=nome, taxa=taxa)); db.commit(); return {"s":"ok"}

@app.delete("/api/admin/bairros/{b_id}")
def del_b(b_id:int, db:Session=Depends(database.get_db), u=Depends(ver_admin)):
    b = db.query(models.Bairro).filter(models.Bairro.id == b_id).first()
    db.delete(b); db.commit(); return {"s":"ok"}
