from pydantic import BaseModel
from typing import Optional
class TaskCreate(BaseModel):
    title: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

class TaskUpdate(BaseModel):
    id: int
    title: str = None
    completed: bool = None

class TaskDelete(BaseModel):
    id: int
    
