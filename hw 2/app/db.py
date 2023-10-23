import asyncpg

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import SQLModel
from sqlalchemy.pool import NullPool

from app.config import db_config

Base = declarative_base()

engine = create_async_engine(
    db_config.DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=True,
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    conn = await asyncpg.connect(user="postgres", password="postgres", database="postgres", host="localhost")
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS public.candidates (
            id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
            name varchar NOT NULL UNIQUE,
            CONSTRAINT candidates_pk PRIMARY KEY (id)
        );
                       
        CREATE TABLE IF NOT EXISTS public.transactions (
            id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
            description varchar NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT transactions_pk PRIMARY KEY (id)
        );
                       
        CREATE TABLE IF NOT EXISTS public.ballot_transactions (
            id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
            ballot_number int NOT NULL,
            CONSTRAINT ballot_transactions_pk PRIMARY KEY (id)
        );
                       
        CREATE TABLE IF NOT EXISTS public.vote_transactions (
            id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,           
            candidate_number int NOT NULL,
            CONSTRAINT vote_transactions_pk PRIMARY KEY (id)
        );

        CREATE TABLE IF NOT EXISTS public.result_transactions (
            id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,           
            candidate_number int NOT NULL,
            vote_count int NOT NULL,
            CONSTRAINT result_transactions_pk PRIMARY KEY (id)  
        );                
                       
        INSERT INTO candidates (name)
        VALUES ('кандидат 1'),
           ('кандидат 2'),
           ('кандидат 3')
        ON CONFLICT (name)
        DO NOTHING;              
    ''')
    await conn.close()
        