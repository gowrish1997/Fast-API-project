from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
from enum import Enum

class CreateTodo(BaseModel):
    content:str=Field(...,description="The content of the todo",min_length=100,max_length=1000)
    is_completed:Optional[bool]=False
