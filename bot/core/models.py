from dataclasses import dataclass
from typing import Optional
import asyncpg


@dataclass
class GuildConfig:
    guild_id: int
    locale: str | None = None
    custom_invite_code: str | None = None
    entry_log_channel_id: int | None = None
    verification_log_channel_id: int | None = None

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "GuildConfig":
        return cls(
            guild_id=record["guild_id"],
            locale=record["locale"],
            custom_invite_code=record["custom_invite_code"],
            entry_log_channel_id=record["entry_log_channel_id"],
            verification_log_channel_id=record["verification_log_channel_id"],
        )

    @classmethod
    async def get(cls, pool: asyncpg.Pool, guild_id: int) -> Optional["GuildConfig"]:
        """Get a guild config from the database.

        Args:
            pool (asyncpg.Pool): The database connection pool.
            guild_id (int): The guild ID to search for.

        Returns:
            Optional[GuildConfig]: The guild config or None if not found.
        """

        query = """
            SELECT * FROM guilds WHERE guild_id = $1
        """
        record = await pool.fetchrow(query, guild_id)
        if record is None:
            return None
        return cls.from_record(record)

    async def save(self, pool: asyncpg.Pool) -> None:
        """Save/update the guild config to the database.
        If the guild config does not exist, it will be created.

        Args:
            pool (asyncpg.Pool): The database connection pool.
        """

        query = """
            INSERT INTO guilds (guild_id, locale, custom_invite_code, entry_log_channel_id, verification_log_channel_id)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (guild_id) DO UPDATE
            SET locale = $2, custom_invite_code = $3, entry_log_channel_id = $4, verification_log_channel_id = $5
        """
        await pool.execute(
            query,
            self.guild_id,
            self.locale,
            self.custom_invite_code,
            self.entry_log_channel_id,
            self.verification_log_channel_id,
        )
