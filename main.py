from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import create_db_and_tables, SessionDep
from sqlmodel import Field, SQLModel, Relationship, select

#Start the app
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

#Define our routes
@app.get("/")
async def root():    
    return {"message": "Hello World"}