from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from models import Entries
from services import engine, create_db_and_tables

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