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


def eval_close(username: str, password: str, reference: str, teacher_initials: str) -> requests.Response:
    url = API_ENDPOINT + "close_eval_and_send_mail/"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"

    payload = {
        "username": username,
        "password": password,
        "refrence": reference,  # Ensure this is spelled correctly as per your API; it might be "reference" instead?
        "teacher_initials": teacher_initials
    }

    response = requests.post(url, json=payload, headers=headers)
    response.encoding = 'utf-8'  # This might be unnecessary if the server correctly specifies the encoding

    return response


def main():
    pass


if __name__ == '__main__':
    main()