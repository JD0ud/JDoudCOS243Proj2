from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import create_db_and_tables, SessionDep
from sqlmodel import Field, SQLModel, Relationship, select
from api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

#Start the app
app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:8000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

#Define our routes
@app.get("/")
async def root():    
    return {"message": "Hello World"}