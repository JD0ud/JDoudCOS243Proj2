from sqlmodel import Field, SQLModel, Relationship, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    playercount: int

class Model1(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    count: int
    active: bool