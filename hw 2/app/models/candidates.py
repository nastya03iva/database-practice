from typing import Optional
from sqlmodel import SQLModel, Field

class Candidates(SQLModel, table=True):
    __tablename__ = 'candidates'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
