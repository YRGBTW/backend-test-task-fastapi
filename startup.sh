#!/bin/sh
python wait_db.py
alembic -c app/alembic.ini upgrade head
python init_roles.py
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
