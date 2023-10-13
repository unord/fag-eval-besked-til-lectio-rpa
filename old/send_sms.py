import datetime

import requests
import json
from decouple import config

#requires a .env file with a api to sms.dk
sms_api_key = config('SMS_API_KEY')

user_cellphone = ["20529367"]

def sms_troubleshooters(this_msg:str):

    for cellphone_number in user_cellphone:
        sms_send(cellphone_number, this_msg)



def sms_send(this_cellphone:str, this_msg:str):
    now = datetime.datetime.now()
    this_msg = f"{now}: {this_msg}"
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

if __name__ == "__main__":
    # execute only if run as a script
    now = datetime.datetime.now()
    try:
        sms_troubleshooters(f"{now}: SMS test worked")
    except:
        print("Something went wrong")
