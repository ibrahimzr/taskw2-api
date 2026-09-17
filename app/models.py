from sqlmodel import SQLModel,Field
from datetime import datetime,timezone
from app.enums import Role,Status,Priority

class Account(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    username:str=Field(max_length=30,unique=True,index=True)
    email:str=Field(unique=True,index=True)
    hashed_password:str
    role:Role=Role.user
    is_active:bool=True

class TaskItem(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    title:str=Field(max_length=120)
    description:str|None=None
    priority:Priority=Priority.medium
    status:Status=Status.todo
    due_date:datetime|None=None
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    user_id:int=Field(foreign_key="account.id",index=True)