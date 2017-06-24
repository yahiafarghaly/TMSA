from __future__ import print_function
import httplib2
import os

import datetime
import time

from apiclient import discovery
from credentials import *
from calendar_api import *
from sheets_api import *
from gmail_api import *
from testcases import *


def main():
    # Google sheet service initialization
    sheets_credentials = sheets_get_credentials()
    sheets_http = sheets_credentials.authorize(httplib2.Http())
    sheets_discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                           'version=v4')
    sheets_service = discovery.build('sheets', 'v4', http=sheets_http,
                                     discoveryServiceUrl=sheets_discoveryUrl)

    # Google calendar service initialization
    calendar_credentials = calendar_get_credentials()
    calendar_http = calendar_credentials.authorize(httplib2.Http())
    calendar_service = discovery.build('calendar', 'v3', http=calendar_http)

    gmail_credentials = gmail_get_credentials()
    gmail_http = gmail_credentials.authorize(httplib2.Http())
    gmail_service = discovery.build('gmail', 'v1', http=gmail_http)


    while(True):
        values = retrieve_first_row(sheets_service)
        if not values:
            print('No data found.')
        else:
            # row[0] => userName
            # row[1] => Date day
            # row[2] => Time
            # row[3] => email account
            # row[4] => TeamID
            # row[5] => Request Type ( 'Reserve' , 'Delete' )
            for row in values:
                startDate,endDate = convert_date_to_iso_format(row[1],row[2])
                team_id = sheets_modify_team_ID(row[4])
                request_res = calendar_is_team_have_successive_requests(calendar_service,startDate,team_id)

                if(request_res == 3 or request_res == 2 or request_res == 1):
                    message = 'You already have another reservation within 2 days. Only 1 time slot is allowed every 2 days.' + os.linesep+ 'Please check the updated calender and reserve another time slot !' + os.linesep + 'No event is created' + os.linesep
                else:
                    if(calendar_is_conflict_v2(calendar_service,startDate,endDate)):
                    	message = 'The time slot you requested is already reserved for another team.' + os.linesep + ' Please check the updated calender and reserve another time slot !' + os.linesep
                        message = message + 'Conflict Time: ' + row[1]+'-'+row[2] + os.linesep
                    else:
                        calendar_create_event(calendar_service,team_id,startDate,endDate)
                        message = 'Reservation Status :  Success '+ os.linesep + 'Time: ' + row[1]+'-'+row[2] + os.linesep

                msg = CreateMessage("dspserver2017@gmail.com", row[3], 'Server Access Request Response(team#' + team_id + ')' ,message)
                SendMessage(gmail_service, "me", msg)
                delete_first_row(sheets_service)
        time.sleep(5) #To avoid exhuasting available quotas


if __name__ == '__main__':
    main()
    #test_calendar_conflict()
