from typing import Optional
from sqlmodel import Field
from app.models.transactions import Transactions

class ResultTransactions(Transactions, table=True):
    __tablename__ = 'result_transcations'
    _id: Optional[int] = Field(default=None, primary_key=True, alias='id') 
    candidate_number: Optional[int]
    vote_count: Optional[int]
