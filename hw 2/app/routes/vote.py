from app.config import db_config
from app.db import get_session
from app.models.candidates import Candidates
from app.models.transactions import Transactions
from app.models.ballot_transactions import BallotTransactions
from app.models.vote_transactions import VoteTransactions
from app.models.result_transactions import ResultTransactions

from fastapi import Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlmodel import select
from sqlalchemy import func
from sqlalchemy.sql import label

from datetime import datetime

router = APIRouter()


@router.post("/get_ballot", status_code=200,
            name="Получение бюллетеня")
async def get_ballot(ballot_number: int, session = Depends(get_session)):
    res = await session.execute(select(BallotTransactions)
                                .where(BallotTransactions.id == ballot_number))
    ballot = res.scalars().first()

    ans = jsonable_encoder(ballot)

    if not ballot:
        db_ballot = BallotTransactions()
        db_ballot.ballot_number = ballot_number
        session.add(db_ballot)
        await session.commit()
        await session.refresh(db_ballot)
        return {f'Такого бюллетеня не существовало. Теперь создан бюллетень {ballot_number}'}
    else:
        db_transaction = Transactions()
        db_transaction.description = "Транзакция получения бюллетеня"
        session.add(db_transaction)
        await session.commit()
        await session.refresh(db_transaction)

        return ans


@router.post("/take_vote", status_code=200,
            name="Проголосовать")
async def take_vote(candidate_number: int, session=Depends(get_session)):
    res = await session.execute(select(Candidates).where(Candidates.id == candidate_number))
    candidate = res.scalars().all()

    if not candidate:
        raise HTTPException(status_code=404, detail="ERROR: такого кандидата не существует")

    db_vote = VoteTransactions()
    db_vote.candidate_number = candidate_number
    session.add(db_vote)
    await session.commit()
    await session.refresh(db_vote)
    db_transaction = Transactions()
    db_transaction.description = "Транзакция голосования"
    session.add(db_transaction)
    await session.commit()
    await session.refresh(db_transaction)

    return {"OK"}


@router.get("/get_results", status_code=200,
            name="Получение итогов")
async def get_results(session=Depends(get_session)):
    res = await session.execute(
        select(Candidates.name, func.count(VoteTransactions.candidate_number).label('count')).\
        outerjoin(VoteTransactions, Candidates.id == VoteTransactions.candidate_number).\
        group_by(Candidates.name).\
        order_by(Candidates.name)
    )

    results = res.fetchall()    
    ans = jsonable_encoder(results)

    db_obj = Transactions()
    db_obj.description = "Транзакция получения итогов"
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)

    return ans


@router.get("/get_all_transactions", status_code=200,
            name="Получение списка всех транзакций")
async def get_all_transactions(session=Depends(get_session)):
    res = await session.execute(select(Transactions))

    results = res.scalars().all()    
    ans = jsonable_encoder(results)

    return ans


@router.get('/get_transaction_count', status_code=200, name='Получение числа транзакций за определенное время', response_model=int)
async def get_transaction_count(start_datetime: datetime, end_datetime: datetime, session = Depends(get_session)):
    res = await session.execute(
        select(func.count(Transactions.id)) 
        .where(Transactions.created_at >= start_datetime)
        .where(Transactions.created_at <= end_datetime)
    )
    
    count = res.scalar()

    return count


@router.get('/votes/count', status_code=200, name='Подсчёт числа голосов за кандидата', response_model=int)
async def get_vote_count(candidate_number: int, session = Depends(get_session)):
    res = await session.execute(select(Candidates).where(Candidates.id == candidate_number))
    candidate = res.scalars().all()

    if not candidate:
        raise HTTPException(status_code=404, detail="ERROR: такого кандидата не существует")
    
    res = await session.execute(
        select(func.count(VoteTransactions.id))
        .where(VoteTransactions.candidate_number == candidate_number)
    )
    
    count = res.scalar()

    return count


def find_max(numbers):
    max_value = max(numbers) 
    idx = [i for i, x in enumerate(numbers) if x == max_value] 
    return idx


@router.get('/get_vote_results', status_code=200, name='победитель/победители')
async def get_vote_results(session = Depends(get_session)):
    res = await session.execute(
        select(Candidates.name, func.count(VoteTransactions.candidate_number).label('count')).\
        outerjoin(VoteTransactions, Candidates.id == VoteTransactions.candidate_number).\
        group_by(Candidates.name).\
        order_by(Candidates.name)
    )

    results = res.fetchall()    
    ans = jsonable_encoder(results)

    result_counts = []
    for item in ans:
        result_counts.append(item['count'])

    idx = find_max(result_counts)

    winners = []
    for i in range(len(ans)):
        if i in idx:
            winners.append(ans[i])

    return winners
