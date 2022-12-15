import requests
from requests.structures import CaseInsensitiveDict
from decouple import config

API_ENDPOINT = "https://lectio-fastapi.herokuapp.com/" #link to fastapi
#API_ENDPOINT = "http://127.0.0.1:8000/" #link to local test fastapi

def send_to_lectio_json_clean_string(this_string: str) -> str:
    this_string = this_string.replace("\n", "##n")
    this_string = this_string.replace("æ", "##ae")
    this_string = this_string.replace("ø", "##oe")
    this_string = this_string.replace("å", "##aa")
    this_string = this_string.replace("Æ", "##AE")
    this_string = this_string.replace("Ø", "##OE")
    this_string = this_string.replace("Å", "##AA")
    return this_string

def lectio_send_msg(lectio_school_id: int, lectio_user: str, lectio_password: str, send_to :str, subject: str, msg: str, msg_can_be_replied: bool):
    url = API_ENDPOINT+"message_send/"
    #print(url)

    msg = send_to_lectio_json_clean_string(msg)
    subject = send_to_lectio_json_clean_string(subject)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    payload = '{"lectio_school_id": "' + str(lectio_school_id)
    payload = payload + '", "lectio_user": "' + lectio_user
    payload = payload + '", "lectio_password": "' + lectio_password
    payload = payload + '", "send_to": "' + send_to
    payload = payload + '", "subject": "' + subject
    payload = payload + '", "msg": "' + msg
    payload = payload + '", "msg_can_be_replied": "' + str(msg_can_be_replied) + '"}'

    resp_post = requests.post(url, data=payload, headers=headers)
    return resp_post

def main():
    lectio_school_id = 235
    lectio_user = config('LECTIO_RPA_USER')
    lectio_password = config('LECTIO_RPA_PASSWORD')
    send_to = 'RPA holdet'
    subject = 'test subject'
    msg = 'test msg'
    msg_can_be_replied = False
    print(lectio_send_msg(lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied).text)



if __name__ == '__main__':
    main()