from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bot_token: str
    supabase_url: str
    supabase_key: str
    webapp_url: str
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


config = Config()
