"""
Drop all tables from a given database
python3 manage.py runscript drop_tables
"""

from django.conf import settings
from django.db import connections, OperationalError


def run():
    if settings.STAGE != "development":
        print("drop_tables can be used only on development environment")
        return

    primary_db = connections["default"]

    try:
        primary_conn = primary_db.cursor()
    except OperationalError as err:
        print(err)
        return None

    try:
        primary_conn.execute(
            "SELECT table_schema,table_name "
            "FROM information_schema.tables "
            "WHERE table_schema = 'public' "
            "ORDER BY table_schema,table_name"
        )
        rows = primary_conn.fetchall()
        for row in rows:
            print("dropping table: ", row[1])
            try:
                primary_conn.execute("drop table " + row[1] + " cascade")
            except Exception as e:
                print("Nothing to worry:", e)
        primary_conn.close()
    except Exception as err:
        print(err)
