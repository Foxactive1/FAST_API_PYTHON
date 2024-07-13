from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas

def create_atleta(db: Session, atleta: schemas.AtletaCreate):
    db_atleta = models.Atleta(**atleta.dict())
    try:
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
        return db_atleta
    except IntegrityError:
        db.rollback()
        raise

def get_atletas(db: Session, nome: str = None, cpf: str = None):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome == nome)
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return query.all()

def get_atleta(db: Session, atleta_id: int):
    return db.query(models.Atleta).filter(models.Atleta.id == atleta_id).first()
