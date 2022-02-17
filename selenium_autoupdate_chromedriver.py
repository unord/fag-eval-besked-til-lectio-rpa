import time
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException, NoSuchElementException
import urllib
from urllib import request
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import platform
from decouple import config
import sys
import datetime
import send_sms

lectio_user = config('LECTIO_RPA_USER')
lectio_password = config('LECTIO_RPA_PASSWORD')
lectio_test_class = config('LECTIO_RPA_TEST_CLASS')
lectio_url_send_msg = config('LECTIO_SEND_MSG_URL')
lectio_url_login = config('LECTIO_LOGIN_URL')

max_try_attempts = 100
try_attempt = 0

currentSite = "https://unord.dk"
win_path = "c:/Chrome"
chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"


def win_download_and_unzip(chromedriver_version_url:str, extract_to='.'):
    download_url:str

    file = urllib.request.urlopen(chromedriver_version_url)
    for line in file:
        decoded_line = line.decode("utf-8")
        download_url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(decoded_line)

    http_response = urlopen(download_url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

def start_browser():
    # Loading webdriver

    osDetect = platform.system() #Check to see if system is windows or osx
    if osDetect == "Darwin": #osx
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(executable_path="/Applications/Chromedriver", options=options)
        return browser
    else: #windows
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            browser = webdriver.Chrome(executable_path="C:\\Chrome\\Chromedriver.exe", options=options)
        except SessionNotCreatedException:
            win_download_and_unzip(chromedriver_version_url, win_path)
            browser = webdriver.Chrome(executable_path="C:\\Chrome\\Chromedriver.exe", options=options)
        except WebDriverException:
            win_download_and_unzip(chromedriver_version_url, win_path)
            browser = webdriver.Chrome(executable_path="C:\\Chrome\\Chromedriver.exe", options=options)
        return browser


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

if __name__ == "__main__":
    # execute only if run as a script

    try:
        browser = start_browser()
        browser.get(currentSite)
        print("Browser connection worked")
        time.sleep(10)
        browser.close()
    except:
        print("Something went wrong")