from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, add_pagination, paginate
from . import models, schemas, database, crud

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/atletas/", response_model=schemas.Atleta)
async def create_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_atleta(db=db, atleta=atleta)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

@app.get("/atletas/", response_model=Page[schemas.Atleta])
async def read_atletas(nome: str = None, cpf: str = None, db: Session = Depends(get_db)):
    return paginate(crud.get_atletas(db=db, nome=nome, cpf=cpf))

@app.get("/atletas/{atleta_id}", response_model=schemas.Atleta)
async def read_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta = crud.get_atleta(db=db, atleta_id=atleta_id)
    if atleta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return atleta

add_pagination(app)
