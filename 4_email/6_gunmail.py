import requests
from account import *

def send_simple_message(email_address):
	print("send message to {0}".format(email_address))

	return requests.post(
		"https://api.mailgun.net/v3/{0}/messages".format(GUMMAIL_DOMAIN),
		auth=("api", API_PRIVATE_KEY),
		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
			"to": [email_address],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomeness!"})


ret = send_simple_message("pidokige0204@gmail.com")
print("ret is {0}".format(ret))