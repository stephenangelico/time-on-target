# Google Calendar integration module
import os
import datetime

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import googleapiclient.errors
import google.auth.exceptions

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CAL_ID = "c7dcbe3c08317dc9ee67fa66d37d67dcf5d8ce265a2ee4c292fb43027649bbeb@group.calendar.google.com"
# How to get calendar ID (After building service): service.calendarList().list().execute()

force_events = []
if "TOT_SIMULATE_EVENT" in os.environ:
	# Fake an event with the given description, one time only
	event_time = datetime.datetime.now().astimezone() + datetime.timedelta(seconds=5)
	force_events = [("synth-event-id", os.environ["TOT_SIMULATE_EVENT"], event_time, (event_time - datetime.datetime.now(tz=datetime.UTC)))]

def main():
	# Error handling is to all be done in tot.py - that way it can be
	# displayed on the LCD. If you are running gcal standalone, you have a
	# console and don't need error handling.
	if force_events:
		return [force_events.pop()]
	creds = Credentials.from_service_account_file("TOT-service-key.json", scopes=SCOPES)
	# TODO: Document setup as it is now in Google Cloud Console
	service = build("calendar", "v3", credentials=creds)
	now = datetime.datetime.now(tz=datetime.UTC).isoformat()
	# Don't reuse this - GCal call may take time
	events = service.events().list(calendarId=CAL_ID, timeMin=now, singleEvents=True, maxResults=15, orderBy="startTime").execute()
	alarms = []
	for event in events["items"]:
		event_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
		alarm = event["id"], event["summary"], event_time, (event_time - datetime.datetime.now(tz=datetime.UTC))
		alarms.append(alarm)
	return alarms

if __name__ == "__main__":
	print(main())
