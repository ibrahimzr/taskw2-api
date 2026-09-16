from enum import Enum

class Role(str,Enum):
    user="user"
    admin="admin"

class Status(str,Enum):
    todo="todo"
    in_progress="in_progress"
    done="done"

class Priority(str,Enum):
    low="low"
    medium="medium"
    high="high"