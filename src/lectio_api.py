import requests
import json
from requests.structures import CaseInsensitiveDict
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

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "lectio_school_id": lectio_school_id,
        "lectio_user": lectio_user,
        "lectio_password": lectio_password,
        "send_to": send_to,
        "subject": subject,
        "msg": msg,
        "msg_can_be_replied": msg_can_be_replied
    })

    resp_post = requests.post(url, json=payload, headers=headers)

    resp_post.encoding = 'utf-8'

    return resp_post.text

def main():
    lectio_school_id = 235
    lectio_user = config('LECTIO_RPA_USER')
    lectio_password = config('LECTIO_RPA_PASSWORD')
    send_to = 'RPA holdet'
    subject = 'test subject'
    msg = 'test msg  æøå öäü ï'
    msg_can_be_replied = False
    print(lectio_send_msg(lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied).text)



if __name__ == '__main__':
    main()