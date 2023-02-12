-- migrate:up

alter table guilds
    alter column locale drop not null;

-- migrate:down

