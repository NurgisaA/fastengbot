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
class WebhookConfigs:
    app_url: str
    webhook_path: str
    webhook_url: str


@dataclass
class Config:
    bot: Bot
    webhook: WebhookConfigs
    db: DB
    settings: Settings


def load_config():
    # TODO: Add some checks here?
    admins_id = []
    if getenv("ADMIN_ID"):
        admins_id = getenv("ADMIN_ID").split(',')

    admins_id = [int(item) for item in admins_id]
    bot_token = getenv("BOT_TOKEN")
    webhook_path = f"/bot/{bot_token}"
    app_url = "https://<your-host>"
    return Config(
        bot=Bot(token=bot_token),
        webhook=WebhookConfigs(
            app_url=app_url,
            webhook_path=webhook_path,
            webhook_url=app_url + webhook_path
        ),
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
