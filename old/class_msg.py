from src import log, postgresql_db
import lectio
import datetime

log_date = datetime.datetime.now()
final_choice_date = "16/03-2022 09:00" # format: dd/mm/yyyy hh:mm
final_reg_date = "10/03-2022 09:00" # format: dd/mm/yyyy hh:mm
final_choice_date = datetime.datetime.strptime(final_choice_date, "%d/%m-%Y %H:%M")
final_reg_date = datetime.datetime.strptime(final_reg_date, "%d/%m-%Y %H:%M")



def main():
    final_reg_date_complete = False


    # Check to see if the current hour has changed
    now = datetime.datetime.now()
    this_hour = now.hour

    log.log(f"The current hour is set to: {this_hour}")
    while True:
        now = datetime.datetime.now()
        if now.hour == this_hour:

            # Test connection
            postgresql_db.psql_test_connection() #test database forbindelse

            # Test to see if final datetime has passed
            if now > final_choice_date:
                log.log("Final datetime has passed. Will check to see if their are not procced tasks that need to be sent.")


                # Get rows from database
                rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id != 3 AND eval_year = 2022")

                if len(rows) <= 0:
                    log.log("Their are no unprocced tasks. Sending status SMS and shutting down program")
                    this_msg = "Final datetime passed and all taskes have been solved. Shutting dwon because of nothing more todo."
                    send_sms.sms_troubleshooters(this_msg)
                    sys.exit()
                # Check to see if any task shoould be run
                else:
                    log.log("Their are unprocced tasks. Starting browser.")
                    browser = selenium_autoupdate_chromedriver.start_browser()
                    lectio.lectio_login(browser)

                    for row in rows:
                        # Send messeges to Lectio
                        # log.log(str(row))
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
                        this_url = row[11]
                        this_sent_status = row[12]
                        this_runtime = row[13]

                        this_message = f"Hej elever for hold: {this_class_element}\n\n"
                        this_message = f"{this_message}Fagevaluering:\n\n"
                        this_message = f"{this_message}Hold: {this_class_element}\n"
                        this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                        this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                        this_message = f"{this_message}Venlig hilsen\nU/NORD"

                        lectio.lectio_send_msg(browser, this_class, this_message)
                        log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

                        # Change state in database to "Shown in Lectio"
                        postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3,
                                                          f"id={row[0]}")
                    log.log("All tasks that are schedueled are complete. Sleepinging for 60s before trying again")
                    log.log("Closeing browser")
                    browser.close()


            elif now > final_reg_date and final_reg_date_complete == False:
                log.log("Final registration date has passed. All evals without registration date set will now be sent sent.")


                # Get rows from database
                rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id == 1 AND eval_year = 2022")

                if len(rows) <= 0:
                    log.log("Their are no evals without registration date set")
                # Check to see if any task shoould be run
                else:
                    log.log("Their are unprocced tasks. Starting browser.")
                    browser = selenium_autoupdate_chromedriver.start_browser()
                    lectio.lectio_login(browser)

                    for row in rows:
                        # Send messeges to Lectio
                        # log.log(str(row))
                        this_id = row[0]
                        this_subject = row[1]
                        this_record_editied = row[2]
                        this_class_element = row[3]
                        this_teacher_name = row[4]
                        this_random = row[5]
                        this_teacher_login = row[6]


if __name__ == "__main__":
    main()


import sys
import time
import selenium_autoupdate_chromedriver, send_sms
import datetime

log_date = datetime.datetime.now()
final_choice_date = "16/03-2022 09:00" # format: dd/mm/yyyy hh:mm
final_reg_date = "10/03-2022 10:53" # format: dd/mm/yyyy hh:mm
final_choice_date = datetime.datetime.strptime(final_choice_date, "%d/%m-%Y %H:%M")
final_reg_date = datetime.datetime.strptime(final_reg_date, "%d/%m-%Y %H:%M")



def main():
    final_reg_date_complete = False

    find_send_errors = False
    if find_send_errors == True:
        postgresql_db.psql_test_connection()
        rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 3 AND eval_year = 2022")
        browser = selenium_autoupdate_chromedriver.start_browser()
        lectio.lectio_login(browser)
        browser.get('https://www.lectio.dk/lectio/239/beskeder2.aspx?type=&laererid=37522669619&selectedfolderid=-70')
        this_link = browser.find_element_by_link_text('Vis alle')
        this_link.click()
        time.sleep(3)
        for row in rows:
            this_class_element = row[3]
            this_class_element = this_class_element[0:14]
            this_class_found = lectio.lectio_does_text_exist(this_class_element, browser)
            if this_class_found != "":
                print(this_class_found)
        browser.close()
        sys.exit()


# Check to see if the current hour has changed
    now = datetime.datetime.now()
    this_hour = now.hour

    log.log(f"The current hour is set to: {this_hour}")
    while True:
        now = datetime.datetime.now()
        if now.hour == this_hour:

            # Test connection
            postgresql_db.psql_test_connection() #test database forbindelse

            # Test to see if final datetime has passed
            if now > final_choice_date:
                log.log("Final datetime has passed. Will check to see if their are not procced tasks that need to be sent.")


                # Get rows from database
                rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id != 3 AND eval_year = 2022")

                if len(rows) <= 0:
                    log.log("Their are no unprocced tasks. Sending status SMS and shutting down program")
                    this_msg = "Final datetime passed and all taskes have been solved. Shutting dwon because of nothing more todo."
                    send_sms.sms_troubleshooters(this_msg)
                    sys.exit()
                # Check to see if any task shoould be run
                else:
                    log.log("Their are unprocced tasks. Starting browser.")
                    browser = selenium_autoupdate_chromedriver.start_browser()
                    lectio.lectio_login(browser)

                    for row in rows:
                        # Send messeges to Lectio
                        # log.log(str(row))
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
                        this_url = row[11]
                        this_sent_status = row[12]
                        this_runtime = row[13]

                        this_message = f"Hej elever for hold: {this_class_element}\n\n"
                        this_message = f"{this_message}Fagevaluering:\n\n"
                        this_message = f"{this_message}Hold: {this_class_element}\n"
                        this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                        this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                        this_message = f"{this_message}Venlig hilsen\nU/NORD"

                        lectio.lectio_send_msg(browser, this_class, this_message)
                        log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

                        # Change state in database to "Shown in Lectio"
                        postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3,
                                                          f"id={row[0]}")
                    log.log("All tasks that are schedueled are complete. Sleepinging for 60s before trying again")
                    log.log("Closeing browser")
                    browser.close()


            elif now > final_reg_date and final_reg_date_complete == False:
                log.log("Final registration date has passed. All evals without registration date set will now be sent sent.")


                # Get rows from database
                rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 1 AND eval_year = 2022")

                if len(rows) <= 0:
                    log.log("Their are no evals without registration date set")
                # Check to see if any task shoould be run
                else:
                    log.log("Their are unprocced tasks. Starting browser.")
                    browser = selenium_autoupdate_chromedriver.start_browser()
                    lectio.lectio_login(browser)

                    for row in rows:
                        # Send messeges to Lectio
                        # log.log(str(row))
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
                        this_url = row[11]
                        this_sent_status = row[12]
                        this_runtime = row[13]

                        this_message = f"Hej elever for hold: {this_class_element}\n\n"
                        this_message = f"{this_message}Fagevaluering:\n\n"
                        this_message = f"{this_message}Hold: {this_class_element}\n"
                        this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                        this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                        this_message = f"{this_message}Venlig hilsen\nU/NORD"

                        lectio.lectio_send_msg(browser, this_class, this_message)
                        log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

                        # Change state in database to "Shown in Lectio"
                        postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3,
                                                          f"id={row[0]}")


                    log.log("All tasks that have not been schedueled have now been sent. Sleepinging for 60s before trying again")
                    log.log("Closeing browser")
                    browser.close()
                final_reg_date_complete = True

            else:

                rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 2 AND eval_open_datetime  < NOW() AND eval_year = 2022")
                if len(rows) > 0:
                    log.log("Their are tasks schedueled. Starting browser.")
                    browser = selenium_autoupdate_chromedriver.start_browser()
                    lectio.lectio_login(browser)




                    for row in rows:


                        # Send messeges to Lectio
                        #log.log(str(row))
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
                        this_message = f"{this_message}Fagevaluering:\n\n"
                        this_message = f"{this_message}Hold: {this_class_element}\n"
                        this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                        this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                        this_message = f"{this_message}Venlig hilsen\nU/NORD"



                        lectio.lectio_send_msg(browser, this_class, this_message)
                        log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

                        # Change state in database to "Shown in Lectio"
                        postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3, f"id={row[0]}")
                    log.log("All tasks that are schedueled are complete. Sleepinging for 60s before trying again")
                    log.log("Closeing browser")
                    browser.close()


                else:
                    log.log("No tasks schedueled. Sleepinging for 60s before trying again")

                    #Wait 60 seconds
                    time.sleep(60)

        else:
            #Send sms  and change hour
            this_msg = "RPA that sends messages via lectio is still running."
            send_sms.sms_troubleshooters(this_msg)
            this_timestamp = datetime.datetime.now()
            log.log(f"sent sms that program is still running.")
            this_hour = now.hour


if __name__ == "__main__":
    main()

                        this_eval_year = this_ = row[7]
                        this_record_created = row[8]
                        this_class_size = [9]
                        this_class = row[10]
                        this_url = row[11]
                        this_sent_status = row[12]
                        this_runtime = row[13]

                        this_message = f"Hej elever for hold: {this_class_element}\n\n"
                        this_message = f"{this_message}Fagevaluering:\n\n"
                        this_message = f"{this_message}Hold: {this_class_element}\n"
                        this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                        this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                        this_message = f"{this_message}Venlig hilsen\nU/NORD"

                        lectio.lectio_send_msg(browser, this_class, this_message)
                        log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

                        # Change state in database to "Shown in Lectio"
                        postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3,
                                                          f"id={row[0]}")
                    log.log("All tasks that have not been schedueled have now been sent. Sleepinging for 60s before trying again")
                    log.log("Closeing browser")
                    browser.close()
                final_reg_date_complete = True

            else:

                rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 2 AND eval_open_datetime  < NOW() AND eval_year = 2022")
                if len(rows) > 0:
                    log.log("Their are tasks schedueled. Starting browser.")
                    browser = selenium_autoupdate_chromedriver.start_browser()
                    lectio.lectio_login(browser)




                    for row in rows:


                        # Send messeges to Lectio
                        #log.log(str(row))
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
                        this_message = f"{this_message}Fagevaluering:\n\n"
                        this_message = f"{this_message}Hold: {this_class_element}\n"
                        this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
                        this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
                        this_message = f"{this_message}Venlig hilsen\nU/NORD"



                        lectio.lectio_send_msg(browser, this_class, this_message)
                        log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

                        # Change state in database to "Shown in Lectio"
                        postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3, f"id={row[0]}")
                    log.log("All tasks that are schedueled are complete. Sleepinging for 60s before trying again")
                    log.log("Closeing browser")
                    browser.close()


                else:
                    log.log("No tasks schedueled. Sleepinging for 60s before trying again")

                    #Wait 60 seconds
                    time.sleep(60)

        else:
            #Send sms  and change hour
            this_msg = "RPA that sends messages via lectio is still running."
            send_sms.sms_troubleshooters(this_msg)
            this_timestamp = datetime.datetime.now()
            log.log(f"sent sms that program is still running.")
            this_hour = now.hour