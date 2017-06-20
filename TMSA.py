from __future__ import print_function
import httplib2
import os

import datetime
import time

from apiclient import discovery
from credentials import sheets_get_credentials
from credentials import calendar_get_credentials
from calendar_api import *
from sheets_api import *
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

    while(True):
        values = retrieve_first_row(sheets_service)
        if not values:
            print('No data found.')
        else:
            # row[0] => userName
            # row[1] => Date day
            # row[2] => Time
            # row[3] => FB account
            # row[4] => TeamID
            # row[5] => Request Type ( 'Reserve' , 'Delete' )
            for row in values:
                startDate,endDate = convert_date_to_iso_format(row[1],row[2])
                team_id = sheets_modify_team_ID(row[4])
                request_res = calendar_is_team_have_successive_requests(calendar_service,startDate,team_id)
                if(request_res == 1):
                    print('You have already reserved for this day')
                elif(request_res == 2):
                    print('You have already reserved for a day before')
                elif(request_res == 3):
                    print('You have already reserved for a day after')
                else:
                    print ("No Reservation Conflict is found")
                    if(calendar_is_conflict_v2(calendar_service,startDate,endDate)):
                        # send fb message
                        print('Team Confict is found for team# ', team_id,'Time: ',row[1]+'-'+row[2])
                    else:
                        # send fb message
                        calendar_create_event(calendar_service,team_id,startDate,endDate)
                        print ('An event is reserved for team#',team_id)
                delete_first_row(sheets_service)
    time.sleep(1)





if __name__ == '__main__':
    main()
    #test_calendar_conflict()
