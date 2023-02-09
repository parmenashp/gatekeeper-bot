import os
from dataclasses import dataclass

_initial_cogs = []


@dataclass(frozen=True)
class BotConfig:
    token: str = os.environ["DISCORD_TOKEN"]
    prefix: str = os.environ["DISCORD_PREFIX"]
    owner_id: int = int(os.environ["DISCORD_OWNER_ID"])
    initial_cogs: list[str] = _initial_cogs


@dataclass(frozen=True)
class Config:
    """Dataclass that holds all the config for the bot."""

    bot: BotConfig = BotConfig()


config = Config()
