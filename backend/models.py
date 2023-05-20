from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Entries(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    title: str
    rank: Optional[int]= Field(default=None)
    points: Optional[int] = Field(default=None)
    comments: Optional[int] = Field(default=None)
