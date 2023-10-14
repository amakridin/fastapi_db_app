DO
$do$
DECLARE
    recreate boolean := {recreate};
BEGIN
    if recreate = true then
        DROP SCHEMA IF EXISTS {db_schema} CASCADE;
        CREATE SCHEMA {db_schema};
    end if;

    SET search_path TO {db_schema};

    CREATE SEQUENCE IF NOT EXISTS user_id_seq;
    CREATE TABLE IF NOT EXISTS users
    (
        id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
        name character varying(256) NOT NULL,
        locale character varying(256) NOT NULL,
        date_created timestamp with time zone NOT NULL DEFAULT now(),
        CONSTRAINT users_pkey PRIMARY KEY (id),
        CONSTRAINT user_name_key UNIQUE (name)
    );

end
$do$