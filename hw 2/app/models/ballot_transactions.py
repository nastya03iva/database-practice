from typing import Optional
from sqlmodel import SQLModel, Field
from app.models.transactions import Transactions

class BallotTransactions(SQLModel, table=True):
    __tablename__ = 'ballot_transactions'
    id: Optional[int] = Field(primary_key=True)
    #transactions_id: Optional[int] = Field(foreign_key='transacions.id') 
    ballot_number: Optional[int]
  