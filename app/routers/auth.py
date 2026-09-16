from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session,select
from app.database import get_session
from app.models import Account
from app.enums import Role
from app.dtos.requests import NewUser
from app.dtos.responses import UserView,TokenData
from app.security import make_hash,check_password,create_token
from app.dependencies import get_current_user

auth_router=APIRouter(prefix="/auth",tags=["Authentication"])

@auth_router.post("/register",response_model=UserView,status_code=status.HTTP_201_CREATED)
def create_account(data:NewUser,session:Session=Depends(get_session)):
    account=session.exec(select(Account).where(Account.username==data.username)).first()
    if account:
        raise HTTPException(status_code=400,detail="Username is taken")

    account=session.exec(select(Account).where(Account.email==data.email)).first()
    if account:
        raise HTTPException(status_code=400,detail="Email is already registered")

    account=Account(username=data.username,email=data.email,hashed_password=make_hash(data.password),role=Role.user)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

@auth_router.post("/login",response_model=TokenData)
def login(form:OAuth2PasswordRequestForm=Depends(),session:Session=Depends(get_session)):
    account=session.exec(select(Account).where(Account.username==form.username)).first()
    if not account or not check_password(form.password,account.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")

    token=create_token(account.id)
    return TokenData(access_token=token,token_type="bearer")

@auth_router.get("/me",response_model=UserView)
def my_account(account:Account=Depends(get_current_user)):
    return account