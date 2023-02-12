import os
from dataclasses import dataclass, field

_initial_cogs = [
    "cogs.guilds",
]


@dataclass(frozen=True)
class BotConfig:
    token: str = os.environ["DISCORD_TOKEN"]
    prefix: str = os.environ["DISCORD_PREFIX"]
    initial_cogs: list[str] = field(default_factory=lambda: _initial_cogs)


@dataclass(frozen=True)
class DbConfig:
    dsn = os.environ["POSTGRES_DSN"]


@dataclass(frozen=True)
class Config:
    """Dataclass that holds all the config for the bot."""

    bot: BotConfig = BotConfig()
    db: DbConfig = DbConfig()


config = Config()
