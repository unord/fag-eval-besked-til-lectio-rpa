from decouple import config
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException, NoSuchElementException
import platform
import send_sms
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
                send_sms.sms_troubleshooters(error_msg)
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
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1


def lectio_send_msg(browser, this_team, this_msg):
    pass