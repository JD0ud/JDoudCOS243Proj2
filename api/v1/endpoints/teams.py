from fastapi import APIRouter, HTTPException
from db.models import Team
from db.session import SessionDep
from sqlmodel import select

router = APIRouter()

@router.get("/")
def get_all_teams(session:SessionDep):
    teams = session.exec(select(Team).order_by(Team.name))
    return teams

@router.get("/{user_id}")
def get_team(team_id:int, session:SessionDep):
    team = None
    team = session.exec(select(Team).where(Team.id == team_id)).first()
    if not team: raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/", status_code=204)
def create_new_team(team:Team, name:str, playercount:int, session:SessionDep):
    new_team = team
    new_team.name = name
    new_team.playercount = playercount
    session.add(new_team)
    session.commit()
    return new_team

@router.put("/", status_code=200)
def edit_team(id:int, name:str, playercount:int, session:SessionDep):
    team = session.exec(select(Team).where(Team.id == id)).first()
    team.name = name
    team.playercount = playercount
    session.commit()
    return team

@router.delete("/", status_code=200)
def delete_team(id:int, session:SessionDep):
    team = None
    team = session.exec(select(Team).where(Team.id == id)).first()
    if not team: raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return team