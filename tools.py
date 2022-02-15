import requests
import json
from decouple import config
from datetime import date, datetime, timedelta


def smsSend(thisCellphone, thisMsg):
    url = "https://api.sms.dk/v1/sms/send"
    payload = json.dumps({
        "receiver": int("45" + str(thisCellphone)),
        "senderName": "U/Nord IT",
        "message": thisMsg,
        "format": "gsm",
        "encoding": "utf8",
      })

    headers = {
     'Authorization': 'Bearer '+ config('SMS_API_KEY'),
     'Content-Type': 'application/json'
     }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
