from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Transactions(SQLModel, table=True):
    __tablename__ = 'transactions'
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    created_at: datetime = datetime.now()
    