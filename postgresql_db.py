import psycopg2
from decouple import config
import send_sms, log
import datetime




# documentation for postgresql: https://stackabuse.com/working-with-postgresql-in-python/

psql_database = config('PSQL_DATABASENAME')
qsql_user = config('PSQL_USER')
qsql_password = config('PSQL_PASSWORD')
qsql_host = config('PSQL_HOST')
qsql_port = config('PSQL_PORT')

psql_table = 'eval_app_classschool'
now = datetime.datetime.now()

def psql_test_connection():
    now = datetime.datetime.now()
    try:
        con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)
        log.log(f"Database opened successfully")
        con.close()
    except:
        error_msg = f"Database connection failed, check credentials"
        log.log(error_msg)
        send_sms.sms_troubleshooters(error_msg)

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
    con = psycopg2.connect(database=psql_database, user=qsql_user, password=qsql_password, host=qsql_host, port=qsql_port)
    this_time = now.strftime("%d-%m-%Y %H:%M:%S")
    cur = con.cursor()
    cur.execute(f"UPDATE {this_table} SET {this_row} = {this_value} WHERE {this_condition}")
    try:
        con.commit()
        log.log(f"Updateing {this_condition} , altered to id_state:{this_value}")
    except:
        error_msg = f"Error in Updateing {this_condition} , to id_state:{this_value}"
        log.log(error_msg)
        tools.smsSend('4591330148', f"{this_time}: "+error_msg)

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
