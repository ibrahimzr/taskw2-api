from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.database import get_session
from app.models import Account
from app.enums import Role
from app.security import read_token
import jwt

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str=Depends(oauth2_scheme),session:Session=Depends(get_session)):
    try:
        data=read_token(token)
        user_id=data.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    account=session.get(Account,user_id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    if not account.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Account is disabled")
    return account

def require_roles(roles:list[Role]):
    def check_role(account:Account=Depends(get_current_user)):
        if account.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")
        return account
    return check_role