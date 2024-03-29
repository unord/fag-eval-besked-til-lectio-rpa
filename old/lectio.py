import time

from decouple import config
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import send_sms
from src import log
import datetime
import sys

lectio_user = config('LECTIO_RPA_USER')
lectio_password = config('LECTIO_RPA_PASSWORD')
lectio_test_class = config('LECTIO_RPA_TEST_CLASS')
lectio_url_send_msg = config('LECTIO_SEND_MSG_URL')
lectio_url_login = config('LECTIO_LOGIN_URL')

max_try_attempts = 100
try_attempt = 0

def lectio_login(browser):
    now = datetime.datetime.now()

    #go to login page
    try:
        browser.get(lectio_url_login)
    except:
        error_msg = "FAG_eval_rpa crashed when trying to access lectio login page"
        send_sms.sms_troubleshooters(error_msg)
        sys.exit()

    #insert username in lectio login, user field
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_username = browser.find_element_by_id("username")
            input_username.send_keys(lectio_user)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts-1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the username in lectio login page"
                log.log("FAG_eval_rpa crashed when trying to type the username in lectio login page")
                send_sms.sms_troubleshooters(error_msg)
                time.sleep(30)
                sys.exit()
            try_attempt = try_attempt + 1

    #insert password in lectio login page, password field
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_password = browser.find_element_by_id("password")
            input_password.send_keys(lectio_password)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts-1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the password in lectio login page"
                log.log("FAG_eval_rpa crashed when trying to type the password in lectio login page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            button_login = browser.find_element_by_id("m_Content_submitbtn2")
            button_login.click()
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts-1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to click the login button in lectio login page"
                log.log("FAG_eval_rpa crashed when trying to click the login button in lectio login page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1


def find_send_msg_error(browser: webdriver):
    find_send_errors = False
    if find_send_errors == True:
        postgresql_db.psql_test_connection()
        rows = postgresql_db.get_all_rows("eval_app_classschool", "eval_sent_state_id = 3 AND eval_year = 2022")
        browser = selenium_tools.get_webdriver()
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


def lectio_send_msg(browser, this_team, this_msg):
    now = datetime.datetime.now()
    #this_team = lectio_test_class #For test only
    this_subject = f"Fagevalueringsundersøgelse for hold: {this_team}"

    # go to lectio send message page
    try:
        browser.get(lectio_url_send_msg)
    except:
        error_msg = "FAG_eval_rpa crashed when trying to access lectio send message page"
        log.log("FAG_eval_rpa crashed when trying to access lectio send message page")
        send_sms.sms_troubleshooters(error_msg)
        sys.exit()

    # insert class in "to field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_class_name = browser.find_element_by_id("s_m_Content_Content_addRecipientDD_inp")
            input_class_name.send_keys(this_team)
            input_class_name.send_keys(Keys.ARROW_DOWN)
            input_class_name.send_keys(Keys.ARROW_DOWN)
            if this_team == "hvhh1c Vø":
                input_class_name.send_keys(Keys.ARROW_DOWN)

            input_class_name.send_keys(Keys.ENTER)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the class_name in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to type the class_name in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # insert message in "subject field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_subject = browser.find_element_by_id("s_m_Content_Content_CreateThreadEditMessageTitle_tb")
            input_subject.send_keys(this_subject)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the subject in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to type the subject in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # checkbox may reply set to unchecked
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            checkbox_may_reply = browser.find_element_by_id("s_m_Content_Content_RepliesToThreadOrExistingMessageAllowedChk")
            if checkbox_may_reply.is_selected():
                checkbox_may_reply.click()
                try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to unclick may reply in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to unclick may reply in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # insert message in "message field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_message = browser.find_element_by_id("s_m_Content_Content_CreateThreadEditMessageContent_TbxNAME_tb")
            input_message.send_keys(this_msg)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the message in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to type the message in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # click submit button

    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            pass
            button_submit = browser.find_element_by_id("s_m_Content_Content_CreateThreadEditMessageOkBtn")
            button_submit.click()
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to click the submit button in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to click the submit button in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1


