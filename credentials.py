# Author:           Yahia Farghaly (yahiafarghaly@outlook.com)
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    sheets_flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    sheets_flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SHEETS_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SHEETS_CLIENT_SECRET_FILE = 'client_secret_sheets.json'
SHEETS_APPLICATION_NAME = 'Google Sheets API Python Quickstart'

try:
    import argparse
    calendar_flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    calendar_flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
CALENDAR_SCOPES = 'https://www.googleapis.com/auth/calendar'
CALENDAR_CLIENT_SECRET_FILE = 'client_secret_calendar.json'
CALENDAR_APPLICATION_NAME = 'Google Calendar API Python Quickstart'



def sheets_get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(SHEETS_CLIENT_SECRET_FILE, SHEETS_SCOPES)
        flow.user_agent = SHEETS_APPLICATION_NAME
        if sheets_flags:
            credentials = tools.run_flow(flow, store, sheets_flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def calendar_get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CALENDAR_CLIENT_SECRET_FILE, CALENDAR_SCOPES)
        flow.user_agent = CALENDAR_APPLICATION_NAME
        if calendar_flags:
            credentials = tools.run_flow(flow, store, calendar_flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials