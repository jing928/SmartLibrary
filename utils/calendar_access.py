import os
import pickle
from datetime import timedelta

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CalendarAccess:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.__service = build('calendar', 'v3', credentials=creds)

    def add_due_date_event(self, title, desc, due_date):
        date_format = '%Y-%m-%d'
        tomorrow = (due_date + timedelta(days=1)).strftime(date_format)
        event = {
            'summary': title,
            'description': desc,
            'start': {
                'date': due_date.strftime(date_format),
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'date': tomorrow,
                'timeZone': 'Australia/Melbourne',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 60},
                ]
            }
        }
        event = self.__service.events().insert(calendarId='primary', body=event).execute()
        event_id = event.get('id')
        return event_id

    def delete_event(self, event_id):
        self.__service.events().delete(calendarId='primary', eventId=event_id).execute()
