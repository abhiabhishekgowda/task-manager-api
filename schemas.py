from pydantic import BaseModel,Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(min_length=3,max_length=50,
    description="the title of the tast")
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="the title of the task",
    )
    completed: Optional[bool] = None

