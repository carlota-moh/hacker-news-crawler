from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from models import Entries
from services import engine, create_db_and_tables
from sqlmodel import Session
from typing import List

# Create FastAPI instance
app = FastAPI()

# define authorization and middleware components
# (for future use in frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost'], # modify with frontend port
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# create database and tables
@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return {"message": "Hello World!"}
       
@app.post('/add-entry/')
def add_entry(entry: Entries):
    with Session(engine) as session:
        exist = session.query(Entries).filter(
            Entries.title == entry.title).first()
        
        if exist:
            raise HTTPException(
                status_code=400, detail="Entry already exists")
        
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

@app.post('/add-entries-bulk/')
def add_bulk_entry(entries: List[Entries]):
    with Session(engine) as session:
        entry_jsons = [entry.dict() for entry in entries]
        session.bulk_insert_mappings(Entries, entry_jsons)
        session.commit()
        return entries

    
@app.get('/entries/')
def get_entries():
    with Session(engine) as session:
        entries = session.query(Entries).all()
        return entries