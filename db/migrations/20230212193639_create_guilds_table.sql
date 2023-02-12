-- migrate:up

create table guilds (
    guild_id bigint not null primary key,
    locale text not null,
    custom_invite_code text,
    entry_log_channel_id bigint,
    verification_log_channel_id bigint
);

-- migrate:down

