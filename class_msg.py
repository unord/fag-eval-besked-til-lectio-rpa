import time

import class_msg, selenium_autoupdate_chromedriver, tools, postgresql_db
import datetime

now = datetime.datetime.now()
test_mode = True

def main():
    # Check to see if the current hour has changed
    this_hour = now.hour
    while True:
        if now.hour == this_hour:
            # Get rows from database
            postgresql_db.psql_test_connection() #test database forbindelse
            rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 2 AND eval_open_datetime  < NOW() AND eval_year = 2022")

            for row in rows:
                # Send messeges to Lectio
                print(row)

                # Change state in database to "Shown in Lectio"
                postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3, f"id={row[0]}")

            #Wait 60 seconds
            time.sleep(60)


        else:
            #Send sms  and change hour
            this_msg = "RPA proggrammet der sender beskeder via lectio kører stadigvæk."
            tools.smsSend('4591330148',this_msg) #GORE
            this_hour = now.hour


if __name__ == "__main__":
    main()