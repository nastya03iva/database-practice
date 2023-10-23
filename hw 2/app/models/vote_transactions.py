from typing import Optional
from sqlmodel import SQLModel, Field
from app.models.transactions import Transactions

class VoteTransactions(SQLModel, table=True):
    __tablename__ = 'vote_transactions'
    id: Optional[int] = Field(default=None, primary_key=True) 
    candidate_number: Optional[int]
