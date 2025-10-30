from fastapi import APIRouter
from api.v1.endpoints import users, teams, model1

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
api_router.include_router(model1.router, prefix="/model1", tags=["Model1"])