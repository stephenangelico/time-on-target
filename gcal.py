# Google Calendar integration module
import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def main():
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
	flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
	creds = flow.run_local_server(port=0)

	# Save tokens
	with open("token.json", "w") as token:
		token.write(creds.to_json())

	#try:
	#	service = build("calendar", "v3", credentials=creds)

if __name__ == "__main__":
	main()
