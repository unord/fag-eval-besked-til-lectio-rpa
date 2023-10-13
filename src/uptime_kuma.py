import requests

def push_health_check(web_address: str) -> None:
    try:
        response = requests.get(web_address, verify=False)
        print(f"Sent health check to uptime-kuma and got the following response {response.status_code}")
    except Exception as e:
        print(e)