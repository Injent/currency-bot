from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    bot_token: str
    currency_api_key: str
    currencies: list[str]
    database: str


env = Env()
env.read_env()

config = Config(
    bot_token=env('BOT_TOKEN'),
    currency_api_key=env('API_KEY'),
    currencies=env('CURRENCIES').split(','),
    database=env('DATABASE')
)