import sys
import psycopg2
from os import getenv
import os
import log
import datetime
import time

# documentation for postgresql: https://stackabuse.com/working-with-postgresql-in-python/

psql_database = getenv('PSQL_DATABASENAME')
qsql_user = getenv('PSQL_USER')
qsql_password = getenv('PSQL_PASSWORD')
qsql_host = getenv('PSQL_HOST')
qsql_port = getenv('PSQL_PORT')

psql_table = 'eval_app_classschool'
now = datetime.datetime.now()

def psql_test_connection():
    try:
        con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)
        log.log(f"Database opened successfully")
        print('Database opened successfully')
        con.close()
    except Exception as e:
        error_msg = f"Database connection failed, check credentials"
        print('error_msg')
        print(f"Error: {e}")
        print(f"Host: {qsql_host}")
        print(f"Port: {qsql_port}")
        print(f"Database: {psql_database}")
        print(f"User: {qsql_user}")
        print(f"Password: {qsql_password}")
        print(os.environ)
        log.log(error_msg)
        time.sleep(600)
        sys.exit(1)


def get_all_rows(this_table=psql_table, this_condition=''):
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)

    cur = con.cursor()
    if this_condition == '':
        cur.execute(f"SELECT * from {this_table}")
    else:
        cur.execute(f"SELECT * from {this_table} WHERE {this_condition}")

    rows = cur.fetchall()
    log.log("Records collected from database")
    con.close()
    log.log("Database connection closed correctly after acquiring records")
    return rows


def update_single_value(this_table, this_row, this_value, this_condition):
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host,
                           port=qsql_port)
    cur = con.cursor()

    query = f"UPDATE {this_table} SET {this_row} = %s WHERE {this_condition}"
    try:
        cur.execute(query, [this_value])
        con.commit()
        log.log(f"Updating {this_condition}, altered to id_state:{this_value}")
    except Exception as e:
        error_msg = f"Error in updating {this_condition}, to id_state:{this_value}. Exception: {e}"
        log.log(error_msg)
    finally:
        cur.close()
        con.close()


def get_all_tables():
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)

    cur = con.cursor()
    cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
    rows = cur.fetchall()

    for row in rows:
        print(row)
    con.close()


def main():
    psql_test_connection()
    print(get_all_rows("eval_app_classschool"))


if __name__ == "__main__":
    main()
