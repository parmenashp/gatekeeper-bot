from dataclasses import dataclass
from typing import Optional
import asyncpg


@dataclass
class GuildConfig:
    guild_id: int
    locale: str | None = None
    use_vanity_invite: bool = False
    custom_invite_code: str | None = None
    entry_log_channel_id: int | None = None
    verification_log_channel_id: int | None = None
    setup_complete: bool = False

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "GuildConfig":
        return cls(
            guild_id=record["guild_id"],
            locale=record["locale"],
            use_vanity_invite=record["use_vanity_invite"],
            custom_invite_code=record["custom_invite_code"],
            entry_log_channel_id=record["entry_log_channel_id"],
            verification_log_channel_id=record["verification_log_channel_id"],
            setup_complete=record["setup_complete"],
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
            INSERT INTO guilds (guild_id, locale, use_vanity_invite, custom_invite_code, entry_log_channel_id, verification_log_channel_id, setup_complete)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (guild_id) DO UPDATE
            SET locale = $2, use_vanity_invite = $3, custom_invite_code = $4, entry_log_channel_id = $5, verification_log_channel_id = $6, setup_complete = $7
        """
        await pool.execute(
            query,
            self.guild_id,
            self.locale,
            self.use_vanity_invite,
            self.custom_invite_code,
            self.entry_log_channel_id,
            self.verification_log_channel_id,
            self.setup_complete,
        )


@dataclass
class JoinGuardConfig:
    guild_id: int
    is_enabled: bool = False
    raid_mode: bool = False
    join_delta: bool = True
    join_delta_threshold: int = 86400  # 1 day
    nitro: bool | None = True
    mobile: bool | None = True
    dm_locked: bool | None = True

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "JoinGuardConfig":
        return cls(
            guild_id=record["guild_id"],
            is_enabled=record["is_enabled"],
            raid_mode=record["raid_mode"],
            join_delta=record["join_delta"],
            join_delta_threshold=record["join_delta_threshold"],
            nitro=record["nitro"],
            mobile=record["mobile"],
            dm_locked=record["dm_locked"],
        )

    @classmethod
    async def get(cls, pool: asyncpg.Pool, guild_id: int) -> Optional["JoinGuardConfig"]:
        """Get a join guard config from the database.

        Args:
            pool (asyncpg.Pool): The database connection pool.
            guild_id (int): The guild ID to search for.

        Returns:
            Optional[JoinGuardConfig]: The join guard config or None if not found.
        """

        query = """
            SELECT * FROM join_guard WHERE guild_id = $1
        """
        record = await pool.fetchrow(query, guild_id)
        if record is None:
            return None
        return cls.from_record(record)

    async def save(self, pool: asyncpg.Pool) -> None:
        """Save/update the join guard config to the database.
        If the join guard config does not exist, it will be created.

        Args:
            pool (asyncpg.Pool): The database connection pool.
        """

        query = """
            INSERT INTO join_guard (guild_id, is_enabled, raid_mode, join_delta, join_delta_threshold, nitro, mobile, dm_locked)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (guild_id) DO UPDATE
            SET is_enabled = $2, raid_mode = $3, join_delta = $4, join_delta_threshold = $5, nitro = $6, mobile = $7, dm_locked = $8
        """
        await pool.execute(
            query,
            self.guild_id,
            self.is_enabled,
            self.raid_mode,
            self.join_delta,
            self.join_delta_threshold,
            self.nitro,
            self.mobile,
            self.dm_locked,
        )
