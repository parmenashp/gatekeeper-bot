import discord
from discord.ext import commands
from loguru import logger
from typing import TYPE_CHECKING
from core import models

from helpers.messages import guild_join_message

if TYPE_CHECKING:
    from main import GatekeeperBot


class Guilds(commands.Cog):
    def __init__(self, bot: "GatekeeperBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        guild_config = await models.GuildConfig.get(self.bot.pool, guild.id)
        first_time = False

        if guild_config is None:
            first_time = True
            guild_config = models.GuildConfig(guild_id=guild.id)
            await guild_config.save(self.bot.pool)

        # Try to send a message to the user who invited the bot by looking at the audit logs.
        if guild.me.guild_permissions.view_audit_log:
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.bot_add, oldest_first=False):
                if entry.target.id == self.bot.user.id and entry.user is not None:  # type: ignore
                    logger.info(
                        f"Joined guild {guild.name} ({guild.id}) {'for the first time ' if first_time else ''}"
                        f"invited by {entry.user.name} ({entry.user.id})"
                    )
                    try:
                        return await entry.user.send(embed=guild_join_message(guild.preferred_locale))
                    except discord.Forbidden:
                        pass

        logger.info(
            f"Joined guild {guild.name} ({guild.id}) {'for the first time ' if first_time else ''}"
            "but could not find a user who invited"
        )

        # If the bot doesn't have permission to view audit logs,
        # send a message to the public updates channel, if it exists.
        if guild.public_updates_channel is not None:
            try:
                return await guild.public_updates_channel.send(embed=guild_join_message(guild.preferred_locale))
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        logger.info(f"Left guild {guild.name} ({guild.id})")


async def setup(bot: "GatekeeperBot"):
    await bot.add_cog(Guilds(bot))
