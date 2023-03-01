#!/usr/bin/env python3

import sys
import getopt
import holidays
import requests
import json
import os.path
import getpass
from datetime import date,datetime
from dateutil.tz import tzlocal
from operator import itemgetter

# aux functions
def getHolidays(company_country, company_subdivision):
    today = date.today().strftime("%Y-%m-%d")
    check_holidays = holidays.country_holidays(company_country, subdiv=company_subdivision)
    get_holidays = check_holidays.get(today)
    if (get_holidays):
        print(get_holidays)
        return True
    else:
        return False

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
    current_time = datetime.now(tzlocal())
    offset_seconds=current_time.utcoffset().total_seconds()
    offset_minutes=offset_seconds/60
    utc_timezone=int(offset_seconds/3600)
    timezone_offset=- + int(offset_minutes)
    utc_timezone_hours='+0{:}'.format(utc_timezone) + ":00"
    #Actually log in
    print("Sending sign request...\n")
    return requests.post(
        f"https://{domain}/api/svc/signs/signs",
        json = {
            'StartDate': datetime.now().replace(microsecond=0).isoformat()+utc_timezone_hours,
            'EndDate': datetime.now().replace(microsecond=0).isoformat()+utc_timezone_hours,
            'TimezoneOffset': timezone_offset,
            'UserId': user_id
        },
        headers = auth_headers
    ).ok

def saveData(username, password, user_id, company_id, company_country, company_subdivision, domain):
    #Store user/password/id to make less network requests in next logins
    with open(inputfile, "w") as login_info:
        json.dump(
            {
                "username": username,
                "password": password,
                "user_id": user_id,
                "company_id": company_id,
                "company_country": company_country,
                "company_subdivision": company_subdivision,
                "domain": domain
            },
            login_info
        )

print("Woffu Autologin Script\n")
def main(argv):
   global inputfile
   inputfile = './data.json'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      print (sys.argv[0] + ' -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (sys.argv[0] + ' -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print ('Input file is ' + inputfile)
   return inputfile
if __name__ == "__main__":
   main(sys.argv[1:])

saved_credentials = os.path.exists(inputfile)
if (saved_credentials):
    with open(inputfile, "r") as json_data:
        login_info = json.load(json_data)
        domain, username, password, user_id, company_id, company_country, company_subdivision = itemgetter(
            "domain",
            "username",
            "password",
            "user_id",
            "company_id",
            "company_country",
            "company_subdivision"
        )(login_info)
else:
    username = input("Enter your Woffu username:\n")
    password = getpass.getpass("Enter your password:\n")

auth_headers = getAuthHeaders(username, password)

if (not saved_credentials):
    domain, user_id, company_id = getDomainUserCompanyId(auth_headers)


if (getHolidays(company_country, company_subdivision)):
    print("Today is a public holiday. What are you doing working?!!. Exiting...")
    exit()


if (signIn(domain, user_id, auth_headers)):
    print ("Success!")
else:
    print ("Something went wrong when trying to log you in/out.")

if (not saved_credentials):
    saveData(username, password, user_id, company_id, domain)
