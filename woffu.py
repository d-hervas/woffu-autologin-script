import requests
import json
import os.path
import getpass
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

def signIn(domain, user_id, auth_headers):
    print("Sending sign request...\n")
    return requests.post(
        f"https://{domain}/api/svc/signs/signs",
        json = {
            'StartDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
            'EndDate': datetime.now().replace(microsecond=0).isoformat()+"+01:00",
            'TimezoneOffset': "-60",
            'UserId': user_id
        },
        headers = auth_headers
    ).ok

def saveData(username, password, user_id, company_id, domain):
    with open("data.json", "w") as login_info:
        json.dump(
            {
                "username": username,
                "password": password,
                "user_id": user_id,
                "company_id": company_id,
                "domain": domain
            },
            login_info
        )

print("Woffu Autologin Script\n")
saved_credentials = os.path.exists("./data.json")
if (saved_credentials):
    with open("./data.json", "r") as json_data:
        login_info = json.load(json_data)
        domain, username, password, user_id, company_id = itemgetter(
            "domain",
            "username",
            "password",
            "user_id",
            "company_id"
        )(login_info)
else:
    username = input("Enter your Woffu username:\n")
    password = getpass.getpass("Enter your password:\n")

auth_headers = getAuthHeaders(username, password)

if (not saved_credentials):
    domain, user_id, company_id = getDomainUserCompanyId(auth_headers)

if (signIn(domain, user_id, auth_headers)):
    print ("Success!")
else:
    print ("Something went wrong when trying to log you in/out.")

if (not saved_credentials):
    saveData(username, password, user_id, company_id, domain)