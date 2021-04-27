QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id text PRIMARY KEY NOT NULL,
    city integer NOT NULL DEFAULT 0,
    stage text NOT NULL DEFAULT 'init'
);
CREATE UNIQUE INDEX users_id_uindex on users (id);
"""