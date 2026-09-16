from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
import jwt
from app.config import app_config

password_hash=PasswordHash.recommended()

def make_hash(password:str):
    return password_hash.hash(password)

def check_password(password:str,hashed_password:str):
    return password_hash.verify(password,hashed_password)

def create_token(user_id:int):
    expire=datetime.now(timezone.utc)+timedelta(minutes=app_config.token_expire_minutes)
    data={"user_id":user_id,"exp":expire}
    return jwt.encode(data,app_config.secret_key,algorithm=app_config.algorithm)

def read_token(token:str):
    return jwt.decode(token,app_config.secret_key,algorithms=[app_config.algorithm])