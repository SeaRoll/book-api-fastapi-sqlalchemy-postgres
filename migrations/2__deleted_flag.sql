alter table books add column if not exists is_deleted boolean not null default false;
