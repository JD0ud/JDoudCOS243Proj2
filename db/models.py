from sqlmodel import Field, SQLModel, Relationship, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str