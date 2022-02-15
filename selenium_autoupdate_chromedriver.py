import time
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import urllib
from urllib import request
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

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