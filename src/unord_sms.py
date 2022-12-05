from decouple import config
import json
import requests


user_cellphone = ["20529367"]

def sms_troubleshooters(this_msg:str):

    for cellphone_number in user_cellphone:
        send_sms(cellphone_number, this_msg)

def send_sms(this_cellphone: str, this_msg: str) -> requests.Response:
    url = "https://api.sms.dk/v1/sms/send"
    payload = json.dumps({
        "receiver": int("45" + str(this_cellphone)),
        "senderName": "U/Nord IT",
        "message": this_msg,
        "format": "gsm",
        "encoding": "utf8",
      })

    headers = {
     'Authorization': 'Bearer ' + config('SMS_API_KEY'),
     'Content-Type': 'application/json'
     }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def main():
    pass


if __name__ == '__main__':
    main()
