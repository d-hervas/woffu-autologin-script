import requests
import json
import os.path
from datetime import datetime
from operator import itemgetter

# aux functions
def getAuthHeaders(username, password):
    # we need to get the Bearer access token for every request we make to Woffu
    print("Getting access token...\n")
    access_token = requests.post(
        "https://app.woffu.com/token",
        data = f"grant_type=password&username={username}&password={password}"
    ).json()['access_token']
    return {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8'
    }

def getDomainUserCompanyId(auth_headers):
    # This function should only be called the first time the script runs.
    # We'll store the results for subsequent executions
    print("Getting IDs...\n")
    users = requests.get(
        "https://app.woffu.com/api/users", 
        headers = auth_headers
    ).json()
    company = requests.get(
        f"https://app.woffu.com/api/companies/{users['CompanyId']}", 
        headers = auth_headers
    ).json()
    return company['Domain'], users['UserId'], users['CompanyId']

print("Woffu Autologin Script\n")
if os.path.exists("./data.json"):
    has_credentials = True
if (has_credentials):
    with open("./data.json", "r") as json_data:
        login_info = json.load(json_data)
        domain, username, password, user_id, signed_in, company_id = itemgetter(
            "domain",
            "username"
            "password",
            "user_id",
            "signed_in",
            "company_id",
        )(login_info)
else:
    username = input("Enter your username:\n")
    password = input("Enter your password:\n")

auth_headers = getAuthHeaders()

if (not has_credentials):
    domain, user_id, company_id = getDomainUserCompanyId(auth_headers)

print("Sending sign request...\n")
signin = requests.post(
    f"https://{domain}/api/svc/signs/signs",
    json = {
        'StartDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
        'EndDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
        'TimezoneOffset': "-60",
        'UserId': user_id
    },
    headers = auth_headers
).status_code

if (not has_credentials):
    with open("data.json", "w") as login_info:
        json.dump(
            {
                "username": username,
                "password": password,
                "signed_in": True,
                "user_id": user_id,
                "company_id": company_id,
                "domain": domain
            },
            login_info
        )
