CREATE SEQUENCE IF NOT EXISTS bot_id_seq;


CREATE TABLE IF NOT EXISTS bots
(
    id integer NOT NULL DEFAULT nextval('bot_id_seq'::regclass),
    bot_id character varying(256) NOT NULL,
    date_created timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT bots_pkey PRIMARY KEY (id),
    CONSTRAINT bot_bot_id UNIQUE (bot_id)
);
