from dataclasses import dataclass
from os import getenv


@dataclass
class Bot:
    token: str


@dataclass
class DB:
    host: str
    db_name: str
    user: str
    password: str


@dataclass
class Settings:
    admin_id: list[int]


@dataclass
class Config:
    bot: Bot
    db: DB
    settings: Settings


def load_config():
    # TODO: Add some checks here?
    admins_id = []
    if getenv("ADMIN_ID"):
        admins_id = getenv("ADMIN_ID").split(',')

    admins_id = [int(item) for item in admins_id]

    return Config(
        bot=Bot(token=getenv("BOT_TOKEN")),

        db=DB(
            host=getenv("DB_HOST"),
            db_name=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASS")
        ),

        settings=Settings(
            admin_id=admins_id
        ),
    )
