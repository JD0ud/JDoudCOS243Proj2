from fastapi import APIRouter, HTTPException, Response, Depends, status
from db.models import User
from db.session import SessionDep
from sqlmodel import select, func, Session

router = APIRouter()

users = [
    {
        "id": 1,
        "name": "Antidisestablishmentarianism"
    },
    {
        "id": 2,
        "name": "Hippopotomonstrosesquippedaliophobia"
    },
    {
        "id": 3,
        "name": "Pneumonoultramicroscopicsilicovolcanoconiosis"
    },
    {
        "id": 4,
        "name": "Supercalifragilisticexpialidocious"
    },
    {
        "id": 5,
        "name": "Floccinaucinihilipilification"
    },
    {
        "id": 6,
        "name": "Pseudopseudohypoparathyroidism"
    },
    {
        "id": 7,
        "name": "Chargoggagoggmanchauggauggagoggchaubunagungamaugg"
    },
    {
        "id": 8,
        "name": "Thyroparathyroidectomized"
    },
    {
        "id": 9,
        "name": "Methylenedioxymethamphetamine"
    },
    {
        "id": 10,
        "name": "Electroencephalographically"
    },
    {
        "id": 11,
        "name": "Radioimmunoelectrophoresis"
    }
]

@router.get("/")
def get_all_users(session:SessionDep, response:Response, perPage:int, curPage: int):
    totalUsers = len(users)
    response.headers["X-Total-Count"] = str(totalUsers)
    # users = session.exec(select(User).order_by(User.id))
    return users[perPage * (curPage - 1) : perPage * curPage]

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

@router.delete("/{user_id}", status_code=200)
def delete_user(user_id:int, session:SessionDep):
    user = None
    # user = session.exec(select(User).where(User.id == user_id)).first()
    user = users[user_id - 1] # TEST CODE
    if not user: raise HTTPException(status_code=404, detail="User not found")
    # session.delete(user)
    users.pop(user_id - 1) # TEST CODE
    session.commit()
    return user