from sqlmodel import SQLModel, create_engine

DATABASE_URL = 'postgresql://postgres:1234@hacker-db:5432/hacker_db'

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)