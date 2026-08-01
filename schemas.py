from pydantic import BaseModel, Field
from typing import Optional

class UserProfile(BaseModel):
    username: str = Field(..., min_length=4, max_length=15)
    age: int
    bio: Optional[str] = Field(None, max_length=100)
    is_active: bool = True