import os

class Settings:
    pg_db = os.environ.get('ATHENAI_PG_DB', "athenai")
    pg_host = os.environ.get('ATHENAI_PG_HOST', "localhost")
    pg_port = int(os.environ.get('ATHENAI_PG_PORT', "5432"))
    pg_user = os.environ.get('ATHENAI_PG_USER', "postgres")
    pg_pass = os.environ.get('ATHENAI_PG_PASS', "")
