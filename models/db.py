from peewee import *
from config.settings import Settings

db = PostgresqlDatabase(Settings.pg_db, user=Settings.pg_user, password=Settings.pg_pass,
                           host=Settings.pg_host, port=Settings.pg_port)
