import psycopg2
from decouple import config
from . import tools

# documentation for postgresql: https://stackabuse.com/working-with-postgresql-in-python/

psql_database = config('PSQL_DATABASENAME')
qsql_user = config('PSQL_USER')
qsql_password = config('PSQL_PASSWORD')
qsql_host = config('PSQL_HOST')
qsql_port = config('PSQL_PORT')

psql_table = 'eval_app_classschool'

def psql_test_connection():
    try:
        con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)
        print("Database opened successfully")
        con.close()
    except:
        error_msg = "Database connection failed, check credentials"
        print(error_msg)
        tools.smsSend('4591330148', error_msg)

def get_all_rows(this_table=psql_table, this_condition=''):
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)

    cur = con.cursor()
    if this_condition == '':
        cur.execute(f"SELECT * from {this_table}")
    else:
        cur.execute(f"SELECT * from {this_table} WHERE {this_condition}")

    rows = cur.fetchall()

    con.close()
    return rows

def update_single_value(this_table, this_row, this_value, this_condition):
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)

    cur = con.cursor()
    cur.execute(f"UPDATE {this_table} SET {this_row} = {this_value} WHERE {this_condition}")
    try:
        con.commit()
        print(f"Updated id: {this_value}, to id_state:{this_condition}")
    except:
        error_msg = f"Error in Updateing id: {this_value}, to id_state:{this_condition}"
        tools.smsSend('4591330148', error_msg)

def get_all_tables():
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)

    cur = con.cursor()
    cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
    rows = cur.fetchall()

    for row in rows:
        print(row)
    con.close()





if __name__ == "__main__":
    psql_test_connection()
