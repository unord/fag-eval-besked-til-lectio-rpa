import requests
import json
from decouple import config

#requires a .env file with a api to sms.dk
sms_api_key = config('SMS_API_KEY')

user_cellphone = ["91330148"]

def sms_troubleshooters(this_msg:str):
    i = 0
    for cellphone_number in user_cellphone:
        sms_send(user_cellphone[i], this_msg)
        i = i + 1


def sms_send(this_cellphone:str, this_msg:str):
    url = "https://api.sms.dk/v1/sms/send"
    payload = json.dumps({
        "receiver": int("45" + str(this_cellphone)),
        "senderName": "U/Nord IT",
        "message": this_msg,
        "format": "gsm",
        "encoding": "utf8",
      })

    headers = {
     'Authorization': 'Bearer '+ sms_api_key,
     'Content-Type': 'application/json'
     }
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
