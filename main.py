from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import create_db_and_tables, SessionDep
from sqlmodel import Field, SQLModel, Relationship, select
from api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

#Start the app
app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

#Define our routes
@app.get("/")
async def root():    
    return {"message": "Hello World"}