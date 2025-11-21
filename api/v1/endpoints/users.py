from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.models import User
from db.session import SessionDep, get_session
from typing import Annotated
from sqlmodel import select, func, Session, col
from pydantic import BaseModel
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")
password_hash = PasswordHash.recommended()

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str

class UserInDB(User):
    hashed_password: str

router = APIRouter()

# users = [
#     {
#         "id": 1,
#         "name": "Antidisestablishmentarianism"
#     },
#     {
#         "id": 2,
#         "name": "Hippopotomonstrosesquippedaliophobia"
#     },
#     {
#         "id": 3,
#         "name": "Pneumonoultramicroscopicsilicovolcanoconiosis"
#     },
#     {
#         "id": 4,
#         "name": "Supercalifragilisticexpialidocious"
#     },
#     {
#         "id": 5,
#         "name": "Floccinaucinihilipilification"
#     },
#     {
#         "id": 6,
#         "name": "Pseudopseudohypoparathyroidism"
#     },
#     {
#         "id": 7,
#         "name": "Chargoggagoggmanchauggauggagoggchaubunagungamaugg"
#     },
#     {
#         "id": 8,
#         "name": "Thyroparathyroidectomized"
#     },
#     {
#         "id": 9,
#         "name": "Methylenedioxymethamphetamine"
#     },
#     {
#         "id": 10,
#         "name": "Electroencephalographically"
#     },
#     {
#         "id": 11,
#         "name": "Radioimmunoelectrophoresis"
#     }
# ]

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
#         "disabled": False,
#     }
# }


def fake_hash_password(password:str):
    return "fakehashed" + password

def get_user(username:str):
    # if username in db:
    #     user_dict = db[username]
    #     return UserInDB(**user_dict)
    user = None
    for session in get_session():
        user = session.exec(select(User).where(User.username == username)).first()
    return user

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def authenticate_user(username:str, password:str):
    user = get_user(username)
    if not user: return False
    if not verify_password(password, user.hashed_password): return False
    return user

def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta: expire = datetime.now(timezone.utc) + expires_delta
    else: expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

def fake_decode_token(token):
    return User(username = token + "fakedecoded", email = "john@example.com", full_name = "John Doe")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # user = fake_decode_token(token)
    # if not user:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("sub")
        if username is None: raise credentials_exception
        token_data = TokenData(username = username)
    except InvalidTokenError: raise credentials_exception
    user = get_user(username = token_data.username)
    if user is None: raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled: raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub": user.username}, expires_delta = access_token_expires)
    return Token(access_token = access_token, token_type = "bearer")

@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/")
def get_all_users(session:SessionDep, response:Response, perPage:int, curPage:int, searchText:str):
    offset = (curPage - 1) * perPage
    statement = select(User).where(col(User.username).ilike(f"%{searchText}")).order_by(User.id).offset(offset).limit(perPage)
    totalUsers = session.query(statement).count()
    response.headers["X-Total-Count"] = str(totalUsers)
    # users = session.exec(select(User).order_by(User.id))
    users1 = session.exec(statement).all()
    return statement

@router.get("/{user_id}")
def get_user(username:str, session:SessionDep):
    user = None
    for session in get_session():
        user = session.exec(select(User).where(User.username == username)).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=204)
def create_new_user(user:User, name:str, session:SessionDep):
    new_user = user
    new_user.username = name
    session.add(new_user)
    session.commit()
    return new_user

@router.put("/", status_code=200)
def edit_user(id:int, name:str, session:SessionDep):
    user = session.exec(select(User).where(User.id == id)).first()
    user.username = name
    session.commit()
    return user

@router.delete("/{user_id}", status_code=200)
def delete_user(user_id:int, session:SessionDep):
    user = None
    user = session.exec(select(User).where(User.id == user_id)).first()
    # user = users[user_id - 1] # TEST CODE
    if not user: raise HTTPException(status_code=404, detail="User not found")
    # session.delete(user)
    # users.pop(user_id - 1) # TEST CODE
    session.commit()
    return user