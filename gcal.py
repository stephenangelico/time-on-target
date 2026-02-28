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

def main():
	creds = None
	if os.path.exists("token.json"): # Keep it simple if we have what we need
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	if not creds or not creds.valid: # Do we have a problem with credentials?
		if creds and creds.expired and creds.refresh_token: # Do we have old creds or no creds?
			creds.refresh(Request()) # If they're old, refresh them.
		else: # If we don't have creds, get them.
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
			# If you don't have the credentials from the Google Cloud Console, there
			# is nothing to be done here. I could make the error prettier but why.
			creds = flow.run_local_server(port=0)
		with open("token.json", "w") as token: # Save creds if we got them
			token.write(creds.to_json())
	service = build("calendar", "v3", credentials=creds)
	now = datetime.datetime.now(tz=datetime.UTC).isoformat()
	# Don't reuse this - GCal call may take time
	events = service.events().list(calendarId=CAL_ID, timeMin=now, singleEvents=True, maxResults=15, orderBy="startTime").execute()
	for event in events["items"]:
		event_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
		print(event["summary"], event_time, (event_time - datetime.datetime.now(tz=datetime.UTC)))
		break # Get only the first event for now

if __name__ == "__main__":
	main()
