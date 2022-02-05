CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email character varying(320) NOT NULL UNIQUE,
    name character varying(250) NOT NULL,
    profile_image integer,
    games jsonb NOT NULL DEFAULT '[]'::jsonb
);
CREATE UNIQUE INDEX users_pkey ON users(id int4_ops);
CREATE UNIQUE INDEX users_email_key ON users(email text_ops);

CREATE TABLE user_sessions (
    token character(255) PRIMARY KEY,
    created timestamp with time zone NOT NULL DEFAULT now(),
    duration interval NOT NULL,
    source text NOT NULL DEFAULT ''::text,
    user_id integer NOT NULL
);
CREATE UNIQUE INDEX user_sessions_pkey ON user_sessions(token bpchar_ops);
CREATE INDEX user_sessions_user_id_index ON user_sessions(user_id int4_ops);

CREATE TABLE parties (
    id SERIAL PRIMARY KEY,
    name character varying(250),
    profile_image integer
);
CREATE UNIQUE INDEX parties_pkey ON parties(id int4_ops);

CREATE TABLE party_member (
    id integer PRIMARY KEY,
    user_id integer NOT NULL,
    party_id integer NOT NULL
);
CREATE UNIQUE INDEX party_member_pkey ON party_member(id int4_ops);
CREATE INDEX party_member_user_index ON party_member(user_id int4_ops);
CREATE INDEX party_member_party_index ON party_member(party_id int4_ops);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    revision text NOT NULL DEFAULT ''::text,
    rules text NOT NULL DEFAULT ''::text,
    profile_image integer,
    custom_fields jsonb DEFAULT '{}'::jsonb,
    creator integer NOT NULL,
    access_level integer NOT NULL DEFAULT 0
);
CREATE UNIQUE INDEX games_pkey ON games(id int4_ops);
CREATE INDEX games_access_level ON games(access_level int4_ops);

CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    type character varying(100) NOT NULL,
    content bytea NOT NULL,
    owner integer NOT NULL
);
CREATE UNIQUE INDEX data_pkey ON data(id int4_ops);

CREATE TABLE game_sessions (
    id SERIAL PRIMARY KEY,
    game integer NOT NULL,
    session_date timestamp with time zone NOT NULL DEFAULT now(),
    session_duration interval NOT NULL DEFAULT '00:00:00'::interval,
    party integer NOT NULL,
    participants jsonb NOT NULL DEFAULT '[]'::jsonb,
    scores jsonb NOT NULL DEFAULT '{}'::jsonb,
    custom_fields jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE UNIQUE INDEX game_sessions_pkey ON game_sessions(id int4_ops);
CREATE INDEX game_sessions_party_index ON game_sessions(party int4_ops);
