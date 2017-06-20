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


def testcase(actual, expected):
    if (actual == expected):
        print("passed")
    else:
        print("failed,actual = ",actual)


def test_calendar_conflict():
    # Google calendar service initialization
    calendar_credentials = calendar_get_credentials()
    calendar_http = calendar_credentials.authorize(httplib2.Http())
    calendar_service = discovery.build('calendar', 'v3', http=calendar_http)

    now = '2017-06-20T00:00:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-20T03:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-20T06:30:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, False)

    now = '2017-06-20T12:00:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-20T13:00:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-20T15:00:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, False)

    now = '2017-06-21T00:00:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, False)

    now = '2017-06-21T03:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, False)

    now = '2017-06-21T13:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-21T12:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-21T11:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, True)

    now = '2017-06-21T09:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, False)

    now = '2017-06-21T08:15:00+02:00'
    x = calendar_is_conflict(calendar_service, startTime=now)
    testcase(x, False)


#  for successive reservation
#     startDate = '2017-06-23T23:05:00+02:00'
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '01')
#     testcase(val,2)
#
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '04')
#     testcase(val,1)
#
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '07')
#     testcase(val,0)
#
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '12')
#     testcase(val,3)
#
#     startDate = '2017-06-24T23:05:00+02:00'
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '02')
#     testcase(val,0)
#
#     startDate = '2017-06-24T25:05:00+02:00'
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '12')
#     testcase(val,1)
#
#     startDate = '2017-06-24T25:05:00+02:00'
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '11')
#     testcase(val,2)
#
#     startDate = '2017-06-25T25:05:00+02:00'
#     val = calendar_is_team_have_successive_requests(calendar_service, startDate, '06')
#     testcase(val,0)

