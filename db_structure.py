QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id text PRIMARY KEY NOT NULL,
    city integer NOT NULL DEFAULT 0,
    stage text NOT NULL DEFAULT 'init'
);
CREATE UNIQUE INDEX users_id_uindex on users (id);

CREATE TABLE IF NOT EXISTS query_log (
    created_at timestamp default current_timestamp,
    user_id text NOT NULL,
    query text NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
"""