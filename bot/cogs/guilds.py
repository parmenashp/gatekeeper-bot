import discord
from discord.ext import commands
from loguru import logger
from typing import TYPE_CHECKING

from helpers.messages import guild_join_message

if TYPE_CHECKING:
    from main import GatekeeperBot


class Guilds(commands.Cog):
    def __init__(self, bot: "GatekeeperBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        # TODO: Create a entry in the database for the guild.
        # TODO: Add a check to see if the bot already has a entry in the database for the guild.

        # Try to send a message to the user who invited the bot by looking at the audit logs.
        if guild.me.guild_permissions.view_audit_log:
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.bot_add):
                if entry.target.id == self.bot.user.id:  # type: ignore
                    logger.info(f"Joined guild {guild.name} ({guild.id}) invited by {entry.user.name} ({entry.user.id})")  # type: ignore
                    try:
                        return await entry.user.send(embed=guild_join_message(guild.preferred_locale))  # type: ignore
                    except discord.Forbidden:
                        pass

        logger.info(f"Joined guild {guild.name} ({guild.id}) but could not find a user who invited")

        # If the bot doesn't have permission to view audit logs,
        # send a message to the public updates channel, if it exists.
        if guild.public_updates_channel is not None:
            try:
                return await guild.public_updates_channel.send(embed=guild_join_message(guild.preferred_locale))  # type: ignore
            except discord.Forbidden:
                pass


async def setup(bot: "GatekeeperBot"):
    await bot.add_cog(Guilds(bot))
