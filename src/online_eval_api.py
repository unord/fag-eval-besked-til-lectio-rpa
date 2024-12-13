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
        "refrence": reference,
        "teacher_initials": teacher_initials
    }

    print(f"Sending request to {url} with payload: {payload}")

    response = requests.post(url, json=payload, headers=headers)
    response.encoding = 'utf-8'

    return response


def test_fasst_api_endpoint():
    # Make sure to replace this URL with the actual URL where your FastAPI application is running
    API_ENDPOINT = "http://10.18.225.150:8081/test_endpoint/"

    # Replace this payload with whatever test data you want to send
    payload = {
        "test_data": "Hello, this is a test."
    }

    # Send a POST request to the test endpoint
    response = requests.post(API_ENDPOINT, json=payload)

    # Print the response JSON to see the echoed back data
    print(response.json())

def main():
    pass


if __name__ == '__main__':
    main()