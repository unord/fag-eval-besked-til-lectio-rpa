import requests
from requests.structures import CaseInsensitiveDict

#API_ENDPOINT = "http://10.127.195.100:8000/" #link to fastapi rpa-03 windows server
#API_ENDPOINT = "http://10.126.225.150:8081/" #link to fastapi rpa-04 linux server
API_ENDPOINT = "http://10.18.225.150:8081/" #link to fastapi rpa-05 linux server


'''
username and password is to login for onlineundersøgelse.dk
reference is the random string in the url for the eval
teacher_initials is the initials of the teacher
'''
def eval_close(username: str, password: str, refrence: str, teacher_initials :str) -> requests.Response:
    url = API_ENDPOINT+"close_eval_and_send_csv/"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json; charset=utf-8"  # specify UTF-8 here

    payload = '{"username": "' + username
    payload = payload + '", "password": "' + password
    payload = payload + '", "refrence": "' + refrence
    payload = payload + '", "teacher_initials": "' + teacher_initials + '"}'

    resp_post = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    resp_post.encoding = 'utf-8'

    return resp_post

def main():
    pass


if __name__ == '__main__':
    main()