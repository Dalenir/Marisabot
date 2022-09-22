create table stats
(
    id      serial
        constraint stats_pk
            primary key,
    time    timestamp,
    points  integer,
    user_id bigint
);

alter table stats
    owner to postgres;

create table users
(
    t_id          bigint                not null
        constraint users_pk
            primary key,
    username      varchar,
    fullname      varchar,
    mood_concern  boolean default false not null,
    tasks_concern boolean default false not null
);

alter table users
    owner to postgres;


create table everyday_tasks
(
    user_id          bigint            not null
        constraint user_fk
            references users,
    task             varchar           not null,
    completed_in_row integer default 0 not null,
    id               serial
        constraint everyday_tasks_pk
            primary key
);

alter table everyday_tasks
    owner to postgres;
