import requests
import json
import os.path
# import pytz
from datetime import datetime
from operator import itemgetter

print("Woffu Autologin Script\n")
if os.path.exists("./data.json"):
    with open("./data.json", "r") as json_data:
        login_info = json.load(json_data)
        # domain, username, password, user_id, signed_in = itemgetter(
        signed_in, password, username = itemgetter(
            # "domain",
            "signed_in",
            "password",
            # "user_id",
            "username"
        )(login_info)
else:
    username = input("Enter your username:\n")
    password = input("Enter your password:\n")
    # insert woffu request
    data = {
        "username": username,
        "password": password,
        "signed_in": False
    }
    with open("data.json", "w") as login_info:
        json.dump(data, login_info)

token_request_data_string = f"grant_type=password&username={username}&password={password}"
token_request = requests.post(
    "https://app.woffu.com/token",
    data = token_request_data_string
)
access_token = token_request.json()['access_token']
auth_headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=utf-8'
    # 'Content-Type': 'application/json'
}

users = requests.get(
    "https://app.woffu.com/api/users", 
    headers = auth_headers
).json()
user_id = users['UserId']
company_id = users['CompanyId']

company = requests.get(
    f"https://app.woffu.com/api/companies/{company_id}", 
    headers = auth_headers
).json()
domain = company['Domain']

signin = requests.post(
    f"https://{domain}/api/svc/signs/signs",
    json = {
        # 'DeviceId': 'WebApp',
        'StartDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
        'EndDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
        'TimezoneOffset': "-60",
        'UserId': user_id
    },
    headers = auth_headers
)

breakpoint