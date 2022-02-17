import time
from decouple import config
import class_msg, selenium_autoupdate_chromedriver, send_sms, postgresql_db
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
            if len(rows) > 0:
                browser = selenium_autoupdate_chromedriver.start_browser()
                selenium_autoupdate_chromedriver.lectio_login(browser)

                for row in rows:
                    # Send messeges to Lectio
                    print(row)
                    this_team:str
                    this_msg:str

                    selenium_autoupdate_chromedriver.lectio_send_msg(browser, this_team, this_msg)

                    # Change state in database to "Shown in Lectio"
                    postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3, f"id={row[0]}")
                browser.close()
            #Wait 60 seconds
            time.sleep(60)

        else:
            #Send sms  and change hour
            this_msg = "RPA proggrammet der sender beskeder via lectio kører stadigvæk."
            send_sms.sms_troubleshooters(this_msg)
            this_hour = now.hour


if __name__ == "__main__":
    main()