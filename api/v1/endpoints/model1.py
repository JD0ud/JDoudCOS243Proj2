from fastapi import APIRouter, HTTPException
from db.models import Model1
from db.session import SessionDep
from sqlmodel import select

router = APIRouter()

@router.get("/")
def get_all_models(session:SessionDep):
    models = session.exec(select(Model1).order_by(Model1.id).order_by(Model1.active))
    return models

@router.get("/{user_id}")
def get_model(model_id:int, session:SessionDep):
    model = None
    model = session.exec(select(Model1).where(Model1.id == model_id)).first()
    if not model: raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.post("/", status_code=204)
def create_new_model(model:Model1, count:int, session:SessionDep):
    new_model = model
    new_model.count = count
    new_model.active = False
    session.add(new_model)
    session.commit()
    return new_model

@router.put("/", status_code=200)
def edit_model(id:int, count: int, active:bool, session:SessionDep):
    model = session.exec(select(Model1).where(Model1.id == id)).first()
    model.count = count
    model.active = active
    session.commit()
    return model

@router.delete("/", status_code=200)
def delete_model(id:int, session:SessionDep):
    model = None
    model = session.exec(select(Model1).where(Model1.id == id)).first()
    if not model: raise HTTPException(status_code=404, detail="Model not found")
    session.delete(model)
    session.commit()
    return model