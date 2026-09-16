from pydantic_settings import BaseSettings,SettingsConfigDict

class ProjectConfig(BaseSettings):
    database_url:str
    secret_key:str
    algorithm:str="HS256"
    token_expire_minutes:int=45
    model_config=SettingsConfigDict(env_file=".env")

app_config=ProjectConfig()