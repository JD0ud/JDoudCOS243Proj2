from sqlmodel import Field, SQLModel, Relationship, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    playercount: int

class Model1(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    count: int
    active: bool