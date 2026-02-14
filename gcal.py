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
CAL_ID = "c7dcbe3c08317dc9ee67fa66d37d67dcf5d8ce265a2ee4c292fb43027649bbeb@group.calendar.google.com"
# How to get calendar ID (After building service): service.calendarList().list().execute()

def get_access_token():
	flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
	creds = flow.run_local_server(port=0)

	# Save tokens
	with open("token.json", "w") as token:
		token.write(creds.to_json())

def main():
	creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# TODO: Proper checking of tokens
	
	service = build("calendar", "v3", credentials=creds)
	calendar_list = service.calendarList().list().execute()
	events = service.events().list(calendarId=CAL_ID, singleEvents=True, maxResults=10, orderBy="startTime").execute()
	for event in events["items"]:
		print(event["summary"], datetime.datetime.fromisoformat(event["start"]["dateTime"]))

if __name__ == "__main__":
	main()
