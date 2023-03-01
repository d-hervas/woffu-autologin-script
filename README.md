# woffu-autologin-script
This is a small script that auto checks you into your Woffu organization.

The point is to schedule this script so that it runs every day at the times you check in and out of work (i.e, 9 and 17)

I don't use it myself at the moment, and I only built it as a fun proof of concept - there are definitely a lot of 
improvements that could be made, rather easily too. However, it does work.

## Why?
A new law in my country is forcing people to check in and out of their jobs, every day at the same hours. Sounds to me
like a boring, useless chore that could be automated, and what is programming if not automating tasks to make our lifes easier.

## How to use
You need Python 3.6+ (f-strings rock!), [the requests library](https://pypi.org/project/requests/) and [the holidays library](https://pypi.org/project/holidays/).

`pip install -r requirements.txt`


You've to configure a data.json file with the following data:
```json
{
  "username": "<YOUR WOFFU USERNAME>",
  "password": "<YOUR WOFFU PASSWORD>",
  "user_id": <YOUR WOFFU USER ID>,
  "company_id": <YOUR COMPANY ID>,
  "company_country": "<YOUR COMPANY COUNTRY>",
  "company_subdivision": "<YOUR COMPANY SUBDIVISION>",
  "domain": "<YOUR COMPANY WOFFU DOMAIN>"
}
```

If you don't have login data in your data.json you'll be prompted to enter your user and password the first time it starts, and that's it, you don't have to do anything else
but to execute the script whenever you want to log in or out.

## Caveats
### Passwords
Be aware, though, this script **STORES YOUR PASSWORD IN PLAIN TEXT IN YOUR COMPUTER**, which is something you should normally never ever
ever do, ever. However, to fully automate the task, I do need the password to send it to the Woffu servers, so I'm afraid there's no way to work around this problem. 

Woffu [does have an API](https://www.woffu.com/wp-content/uploads/2021/07/Woffu_API_Document__Guide_en.pdf) your organization 
can probably use to log you in, or enable so that your user can have an API Key or something. The organization I used to test
this script doesn't so this script is the only way to do it, to my knowledge. If you want to use this script and you want it
to be compatible with your API Key instead of using your password (you should want to!), open an issue and I'll probably do it,
it should be really easy.

