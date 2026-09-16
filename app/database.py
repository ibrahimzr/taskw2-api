from sqlmodel import SQLModel,create_engine,Session
from app.config import app_config

db_engine=create_engine(app_config.database_url,connect_args={"check_same_thread":False})

def get_session():
    with Session(db_engine) as session:
        yield session

def setup_db():
    SQLModel.metadata.create_all(db_engine)

