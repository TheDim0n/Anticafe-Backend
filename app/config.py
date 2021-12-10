from pydantic import BaseSettings


class Settings(BaseSettings):
    # database settings
    database_url: str

    # main app settings
    debug: bool = False
    secret_key: str
    default_admin_login: str
    default_admin_password: str
    access_token_expire_minutes: int

    # proxy settings
    root_path: str = ''

    class Config:
        env_file = ".env"
