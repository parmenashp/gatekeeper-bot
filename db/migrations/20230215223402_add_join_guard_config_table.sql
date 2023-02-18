-- migrate:up

create table if not exists join_guard (
    guild_id bigint not null primary key references guilds (guild_id),
    is_enabled bool not null default false,
    raid_mode bool not null default false,
    join_delta bool not null default true,
    join_delta_threshold int not null default 86400,
    nitro bool not null default true,
    mobile bool not null default true,
    dm_locked bool not null default true
);

-- migrate:down

