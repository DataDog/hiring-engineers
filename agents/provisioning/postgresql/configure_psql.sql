create user :dduser with password :'ddpassword';
grant pg_monitor to datadog;

create table tweets(
    id bigint PRIMARY KEY NOT NULL,
    userid text,
    username text,
    created_at text,
    text text,
    full_text text
);

create user vagrant with password 'vagrant';
grant all privileges on database postgres to vagrant;
grant all privileges on all tables in schema public to vagrant;