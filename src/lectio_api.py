import requests
import json
from requests.structures import CaseInsensitiveDict
from os import getenv
from decouple import config

API_ENDPOINT = "https://lectio-fastapi.herokuapp.com/" #link to fastapi
#API_ENDPOINT = "http://127.0.0.1:8000/" #link to local test fastapi

def send_to_lectio_json_clean_string(this_string: str) -> str:
    this_string = this_string.replace("\n", "##n")
    print(this_string)
    return this_string


def lectio_send_msg(
        lectio_school_id: int,
        lectio_user: str,
        lectio_password: str,
        send_to: str,
        subject: str,
        msg: str,
        msg_can_be_replied: bool
):
    url = f"{API_ENDPOINT}message_send/"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json; charset=utf-8"  # specify UTF-8 here

    payload = json.dumps({
        "lectio_school_id": lectio_school_id,
        "lectio_user": lectio_user,
        "lectio_password": lectio_password,
        "send_to": send_to,
        "subject": subject,
        "msg": msg,
        "msg_can_be_replied": msg_can_be_replied
    }, ensure_ascii=False)  # set ensure_ascii to False to handle non-ASCII characters

    resp_post = requests.post(url, data=payload.encode('utf-8'), headers=headers)  # encode payload explicitly to UTF-8

    resp_post.encoding = 'utf-8'

    return resp_post.text

def main():
    lectio_school_id = 235
    lectio_user = getenv('LECTIO_RPA_USER')
    lectio_password = getenv('LECTIO_RPA_PASSWORD')
    send_to = 'Michael Corey Zieler'
    subject = 'test subject'
    msg = 'test msg  æøå öäü ï'
    msg_can_be_replied = False
    print(lectio_send_msg(lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied))


if __name__ == '__main__':
    main()