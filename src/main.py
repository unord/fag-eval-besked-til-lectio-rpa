import sys
import log, postgresql_db, unord_sms, lectio_api, online_eval_api, unord_mail, uptime_kuma
import datetime
from os import getenv
import time
import traceback

lectio_user = getenv('LECTIO_RPA_USER')
lectio_password = getenv('LECTIO_RPA_PASSWORD')
eval_user = getenv('EVAL_RPA_USER')
eval_password = getenv('EVAL_RPA_PASSWORD')

log_date = datetime.datetime.now()
final_choice_date = "05/12-2029 12:15" # format: dd/mm/yyyy hh:mm
final_reg_date = "05/12-2029 12:10" # format: dd/mm/yyyy hh:mm
final_choice_date = datetime.datetime.strptime(final_choice_date, "%d/%m-%Y %H:%M")
final_reg_date = datetime.datetime.strptime(final_reg_date, "%d/%m-%Y %H:%M")

lectio_login_url ="https://www.lectio.dk/lectio/236/login.aspx"

uptime_kuma_url = "http://10.18.225.150:8005/api/push/oWmayS87M8?status=up&msg=OK&ping="


def if_final_datetime_passed(final_datetime):
    log.log("Final datetime has passed. Will check to see if their are not procced tasks that need to be sent.")

    # Get rows from database
    rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id != 3")

    if len(rows) <= 0:
        log.log("Their are no unprocced tasks. Sending status SMS and shutting down program")
        this_msg = "Final datetime passed and all taskes have been solved. Shutting down because of nothing more todo."
        unord_sms.sms_troubleshooters(this_msg)
        sys.exit()
    # Check to see if any task shoould be run
    else:
        log.log("Their are unprocced tasks. Starting browser.")
        #browser = selenium_tools.get_webdriver()
        #lectio.lectio_login(browser)

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
            this_record_created = row[7]
            this_class_size = [8]
            this_class = row[9]
            this_url = row[10]
            this_sent_status = row[11]
            this_runtime = row[12]

            this_message = f"Hej elever for hold: {this_class_element}\n\n"
            this_message = f"{this_message}Fagevaluering:\n\n"
            this_message = f"{this_message}Hold: {this_class_element}\n"
            this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
            this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
            this_message = f"{this_message}Venlig hilsen\nU/NORD"


            lectio_fastapi_msg = lectio_api.lectio_send_msg(234, lectio_user, lectio_password, this_class_element, f"Fagevaluering for hold: {this_class_element}", this_message, False)
            log.log(f'Msg for lectio-fastapi: {lectio_fastapi_msg}')
            log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

            # Change state in database to "Shown in Lectio"
            postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3,
                                              f"id={row[0]}")
        log.log("All tasks that are schedueled are complete. Sleepinging for 60s before trying again")


def final_datetime_passed_sending_the_rest():
    log.log("Final registration date has passed. All evals without registration date set will now be sent sent.")

    # Get rows from database
    rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 1")

    if len(rows) <= 0:
        log.log("Their are no evals without registration date set")
    # Check to see if any task shoould be run
    else:
        log.log("Their are unprocced tasks. Starting browser.")
        #browser = selenium_tools.get_webdriver()
        #lectio.lectio_login(browser)

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
            this_record_created = row[7]
            this_class_size = [8]
            this_class = row[9]
            this_url = row[10]
            this_sent_status = row[11]
            this_runtime = row[12]

            this_message = f"Hej elever for hold: {this_class_element}\n\n"
            this_message = f"{this_message}Fagevaluering:\n\n"
            this_message = f"{this_message}Hold: {this_class_element}\n"
            this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
            this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
            this_message = f"{this_message}Venlig hilsen\nU/NORD"


            lectio_fastapi_msg = lectio_api.lectio_send_msg(234, lectio_user, lectio_password, this_class, f"Fagevaluering for hold: {this_class_element}", this_message, False)
            log.log(f'Msg for lectio-fastapi: {lectio_fastapi_msg}')
            log.log(f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")

            # Change state in database to "Shown in Lectio"
            postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3,
                                              f"id={row[0]}")

        log.log("All tasks that have not been schedueled have now been sent. Sleepinging for 60s before trying again")



def sending_scheduled_evals():
    rows = postgresql_db.get_all_rows("eval_app_classschool",
                                      "eval_sent_state_id = 2 AND eval_open_datetime  < NOW()")
    if len(rows) > 0:
        log.log("Their are tasks schedueled. Starting browser.")
        #browser = selenium_tools.get_webdriver()
        #lectio.lectio_login(browser)

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
            this_record_created = row[7]
            this_class_size = [8]
            this_class = row[9]
            this_url = row[10]
            this_sent_status = row[11]
            this_runtime = row[12]

            this_message = f"Hej elever for hold: {this_class_element}\n\n"
            this_message = f"{this_message}Fagevaluering:\n\n"
            this_message = f"{this_message}Hold: {this_class_element}\n"
            this_message = f"{this_message}Lærer for holdet: {this_teacher_name}, ({this_teacher_login})\n\n"
            this_message = f'{this_message}Link til online skema: [url={this_url}]Fagevaluering: {this_class_element} - {this_subject}[/url]\n\n'
            this_message = f"{this_message}Venlig hilsen\nU/NORD"


            lectio_fastapi_msg = lectio_api.lectio_send_msg(236, lectio_user, lectio_password, this_class_element, f"Fagevaluering for hold: {this_class_element}", this_message, False)
            if 'success' in lectio_fastapi_msg and lectio_fastapi_msg['success'] == True:
                postgresql_db.update_single_value("eval_app_classschool", "eval_sent_state_id", 3, f"id={row[0]}")
                log.log(f'Msg for lectio-fastapi: {lectio_fastapi_msg}')

                log.log(
                    f"Sent message about this class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")
            else:
                error_msg = f"Failed to to send msg via lectio for class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}"
                log.log(error_msg)
                unord_mail.send_email_with_attachments('ubot@unord.dk', ['gore@unord.dk'], f'Failed to send msg via lectio for class: {this_class_element}', error_msg, [], [], [])




            # Change state in database to "Shown in Lectio"




    else:
        log.log("No tasks schedueled. Sleepinging for 60s before trying again")


def final_reg_date_complete_state(now: datetime.datetime, final_reg_date: datetime.datetime) -> bool:
    return now > final_reg_date


def close_evals_scheduled() -> None:
    rows = postgresql_db.get_all_rows("eval_app_classschool",
                               "eval_sent_state_id = 3 "
                               "AND eval_close_datetime IS NOT NULL "
                               "AND eval_close_datetime < NOW() "
                               "AND eval_closed = False")
    if len(rows) > 0:
        for row in rows:
            this_id = row[0]
            this_subject = row[1]
            this_record_editied = row[2]
            this_class_element = row[3]
            this_teacher_name = row[4]
            this_random = row[5]
            this_teacher_login = row[6]
            this_record_created = row[7]
            this_class_size = [8]
            this_class = row[9]
            this_url = row[10]
            this_sent_status = row[11]
            this_runtime = row[12]

            log.log(f"sending data to eval-api: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")
            msg = online_eval_api.eval_close(eval_user, eval_password, this_random, this_teacher_login)
            log.log(f"msg from eval-api: {msg}")
            if msg.status_code == 200:
                postgresql_db.update_single_value("eval_app_classschool", "eval_closed", True, f"id={this_id}")
                log.log(f"Closed eval for class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}")
            else:
                error_msg = f"Failed to close eval for class: {this_class_element}, with this teacher: {this_teacher_name} ({this_teacher_login}) and this key{this_random}"
                log.log(error_msg)
                unord_mail.send_email_with_attachments('ubot@unord.dk', ['gore@unord.dk'], f'Failed to close eval for class: {this_class_element}', error_msg, [], [], [])


def main():
    print(log_date)
    try:
        while True:
            postgresql_db.psql_test_connection()  # test database forbindelse

            #browser = selenium_tools.get_webdriver()
            #lectio.find_send_msg_error(browser)

            now = datetime.datetime.now()
            #now = datetime.datetime.strptime(now, "%d/%m-%Y %H:%M")
            final_reg_date_complete = final_reg_date_complete_state(now, final_reg_date)


            # Test to see if final datetime has passed
            if now > final_choice_date:
                if_final_datetime_passed(final_choice_date)
            # Test to see if final registration time has passed
            elif final_reg_date_complete == True:
                final_datetime_passed_sending_the_rest()

            sending_scheduled_evals()
            close_evals_scheduled()

            uptime_kuma.push_health_check(uptime_kuma_url)

            log.log("Sleeping for 60s before trying again")
            time.sleep(60)

    except Exception as e:
        error_msg = f"Error in main loop: {e}"
        log.log(error_msg)
        log.log(traceback.print_exc())
        time.sleep(600)
        sys.exit()

if __name__ == "__main__":
    main()

