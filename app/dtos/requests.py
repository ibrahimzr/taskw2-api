from sqlmodel import SQLModel,Field
from pydantic import field_validator,EmailStr
from datetime import datetime,timezone
from app.enums import Priority

class NewUser(SQLModel):
    username:str=Field(min_length=3,max_length=30)
    email:EmailStr
    password:str=Field(min_length=8)

class NewTask(SQLModel):
    title:str=Field(min_length=1,max_length=120)
    description:str|None=None
    priority:Priority=Priority.medium
    due_date:datetime|None=None

    @field_validator("title")
    @classmethod
    def check_title(cls,value):
        if not value.strip():
            raise ValueError("TITLE_VALIDATION_17")
        return value.strip()

    @field_validator("due_date")
    @classmethod
    def check_date(cls,value):
        if value is not None:
            check_value=value
            if check_value.tzinfo is None:
                check_value=check_value.replace(tzinfo=timezone.utc)
            if check_value<datetime.now(timezone.utc):
                raise ValueError("Due date cannot be in the past")
        return value

class TaskEdit(SQLModel):
    title:str|None=Field(default=None,min_length=1,max_length=120)
    description:str|None=None
    priority:Priority|None=None
    due_date:datetime|None=None

    @field_validator("title")
    @classmethod
    def check_title(cls,value):
        if value is not None and not value.strip():
            raise ValueError("TITLE_VALIDATION_17")
        return value.strip() if value else value

    @field_validator("due_date")
    @classmethod
    def check_date(cls,value):
        if value is not None:
            check_value=value
            if check_value.tzinfo is None:
                check_value=check_value.replace(tzinfo=timezone.utc)
            if check_value<datetime.now(timezone.utc):
                raise ValueError("Due date cannot be in the past")
        return value