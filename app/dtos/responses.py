from sqlmodel import SQLModel
from datetime import datetime
from app.enums import Role,Status,Priority

class UserView(SQLModel):
    id:int
    username:str
    email:str
    role:Role
    is_active:bool

class TokenData(SQLModel):
    access_token:str
    token_type:str

class TaskView(SQLModel):
    id:int
    title:str
    description:str|None=None
    priority:Priority
    status:Status
    due_date:datetime|None=None
    created_at:datetime
    user_id:int