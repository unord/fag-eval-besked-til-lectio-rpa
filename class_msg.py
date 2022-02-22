import time
import selenium_autoupdate_chromedriver, send_sms, postgresql_db, lectio
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
                lectio.lectio_login(browser)




                for row in rows:


                    # Send messeges to Lectio
                    print(row)
                    this_id = row[0]
                    this_subject = row[1]
                    this_record_editied = row[2]
                    this_class_element = row[3]
                    this_teacher_name = row[4]
                    this_random = row[5]
                    this_teacher_login = row[6]
                    this_eval_year = this_ = row[7]
                    this_record_created = row[8]
                    this_class_size = [9]
                    this_class = row[10]
                    this_url =row[11]
                    this_sent_status = row[12]
                    this_runtime = row[13]



                    this_message = f"Hej elever for hold: {this_class_element}\n\n"
                    this_message = f"{this_message}Jeres evaluerings skema er klar til at blive besvaret for:\n\n"
                    this_message = f"{this_message}Hold: {this_class_element}\n"
                    this_message = f"{this_message}Underviser ansvarligt for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                    this_message = f"{this_message}U/Nord sætter stor pris på at du besvare dette spørgeskema hurtigst muligt og inde den 03/10-2022\n\n"
                    this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                    this_message = f"{this_message}mvh U/Nord"



                    lectio.lectio_send_msg(browser, this_class, this_message)

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