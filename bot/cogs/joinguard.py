import discord
from discord.ext import commands
from loguru import logger
from helpers import utils
from typing import TYPE_CHECKING
from core import models

if TYPE_CHECKING:
    from main import GatekeeperBot


def created_join_delta(member: discord.Member) -> float:
    # There are some edge cases where discord doesn't send the joined_at
    if member.joined_at is None:
        return 0
    return (member.created_at - member.joined_at).total_seconds()


class JoinGuard(commands.Cog):
    def __init__(self, bot: "GatekeeperBot") -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        logger.debug(f"Member {member} joined guild {member.guild}")

        config = await models.JoinGuardConfig.get(self.bot.pool, member.guild.id)
        if config is None or not config.is_enabled:
            return
        await self._check_joining_member(member, config)

    async def _check_joining_member(self, member: discord.Member, config: models.JoinGuardConfig):
        if member.is_on_mobile() and config.mobile:
            pass

        if created_join_delta(member) < config.join_delta_threshold and config.join_delta:
            pass

        # To check if the user is nitro require a api call,
        # so we only do it if the config is enabled to save api calls
        if config.nitro:
            if await utils.guess_if_user_is_nitro(self.bot, member):
                pass

        # Again to save on rate limits
        if config.dm_locked:
            if await utils.is_dm_open(member):
                pass


async def setup(bot: "GatekeeperBot"):
    await bot.add_cog(JoinGuard(bot))
