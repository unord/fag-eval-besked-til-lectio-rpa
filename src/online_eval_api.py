import requests
from requests.structures import CaseInsensitiveDict

API_ENDPOINT = "https://lectio-fastapi.herokuapp.com/" #link to fastapi


'''
username and password is to login for onlineundersøgelse.dk
reference is the random string in the url for the eval
teacher_initials is the initials of the teacher
'''
def eval_close(username: str, password: str, refrence: str, teacher_initials :str) -> requests.Response:
    url = API_ENDPOINT+"close_eval_and_send_csv/"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    payload = '{"username": "' + str(username)
    payload = payload + '", "password": "' + password
    payload = payload + '", "refrence": "' + refrence
    payload = payload + '", "teacher_initials": "' + teacher_initials + '"}'

    resp_post = requests.post(url, data=payload, headers=headers)
    return resp_post

def main():
    pass


if __name__ == '__main__':
    main()