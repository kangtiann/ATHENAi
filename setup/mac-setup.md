# Mac Setup

## Install Postgres

```bash
brew install postgresql
brew services start postgresql

psql -d postgres
```

## Set Env

```bash
export PYTHONPATH=xxxx/ATHENAi:$PYTHONPATH

# AI
export DEEPSEEK_API_KEY=xxx


# reddit
export REDDIT_CLIENT_ID=xxx
export REDDIT_CLIENT_SECRET=-xxx
export REDDIT_USERNAME=xxx
export REDDIT_PASSWORD=xxx

# ATHENAi
export ATHENAI_PG_DB="athenai"
export ATHENAI_PG_HOST="localhost"
export ATHENAI_PG_PORT="5432"
export ATHENAI_PG_USER="xxx"
export ATHENAI_PG_PASS=""
```

## Install npm

```bash
brew install node

npm install @mui/material @emotion/react @emotion/styled @mui/icons-materia
```

## Install Python Packages

```bash
.venv/bin/pip install -r requirements.txt
```

## Start API Server


Init Databases:
```bash
psql postgres

create database athenai
```

```bash
source .venv/bin/activate
python init_database.py
```

Start server:
```bash
bash api/start-api.sh
```

When Drop database: DETAIL:  There is 1 other session using the database.
Kill ATHENAi process.
```bash
SELECT 
    pg_terminate_backend(pid) 
FROM 
    pg_stat_activity 
WHERE 
    pid <> pg_backend_pid()
    AND datname = 'athenai'
    ;
```