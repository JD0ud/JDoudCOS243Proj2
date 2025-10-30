from fastapi import APIRouter, HTTPException
from db.models import User
from db.session import SessionDep
from sqlmodel import select

router = APIRouter()

@router.get("/")
def get_all_users(session:SessionDep):
    users = session.exec(select(User).order_by(User.id))
    return users

@router.get("/{user_id}")
def get_user(user_id:int, session:SessionDep):
    user = None
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=204)
def create_new_user(user:User, name:str, session:SessionDep):
    new_user = user
    new_user.name = name
    session.add(new_user)
    session.commit()
    return new_user

@router.put("/", status_code=200)
def edit_user(id:int, name:str, session:SessionDep):
    user = session.exec(select(User).where(User.id == id)).first()
    user.name = name
    session.commit()
    return user

@router.delete("/", status_code=200)
def delete_user(id:int, session:SessionDep):
    user = None
    user = session.exec(select(User).where(User.id == id)).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user