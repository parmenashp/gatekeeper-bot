-- migrate:up

ALTER TABLE guilds ADD COLUMN use_vanity_invite BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE guilds ADD COLUMN setup_complete BOOLEAN NOT NULL DEFAULT FALSE;

-- migrate:down

ALTER TABLE guilds DROP COLUMN use_vanity_invite;
ALTER TABLE guilds DROP COLUMN setup_complete;