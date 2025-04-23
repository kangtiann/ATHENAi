import os

class Settings:
    pg_db = os.environ.get('ATHENA1_PG_DB', "public.athena1")
    pg_host = os.environ.get('ATHENA1_PG_HOST', "localhost")
    pg_port = int(os.environ.get('ATHENA1_PG_PORT', "5432"))
    pg_user = os.environ.get('ATHENA1_PG_USER', "postgres")
    pg_pass = os.environ.get('ATHENA1_PG_PASS', "")


