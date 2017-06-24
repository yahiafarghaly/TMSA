from sheets_api import sheets_modify_team_ID
# Author:           Yahia Farghaly (yahiafarghaly@outlook.com)
# Usage Example:
# calendar_create_event(calendar_service,'2',
#                       '2017-06-20T17:00:00+02:00','2017-06-20T18:00:00+02:00')
def calendar_create_event(service, teamID, startTime, endTime):
    event = {
        'summary': 'Team#' + teamID,
        'location': 'Egypt@RDI',
        'description': 'Reserved time slot',
        'start': {
            'dateTime': startTime,  # isoformat '2017-06-20T17:00:00+02:00'
            'timeZone': 'Africa/Cairo',  # or EET
        },
        'end': {
            'dateTime': endTime,
            'timeZone': 'Africa/Cairo',
        },
    }
    event = service.events().insert(calendarId='pfua0o0tbak5vhcbjlq5vqbe50@group.calendar.google.com',
                                    body=event).execute()
    #print ('Event created: %s' % (event.get('htmlLink')))
    # the public link for this calendar: https://calendar.google.com/calendar/embed?src=pfua0o0tbak5vhcbjlq5vqbe50%40group.calendar.google.com&ctz=Africa/Cairo

#usage Example: calendar_is_conflict(calendar_service,startTime = '2017-06-20T11:00:00+02:00')
# more general method and may fail at any cornor case
def calendar_is_conflict(calendar_service, startTime):
    eventsResult = calendar_service.events().list(
        calendarId='pfua0o0tbak5vhcbjlq5vqbe50@group.calendar.google.com', timeMin=startTime, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        return False
    else:

        for event in events:
            comingEvent_start = event['start'].get('dateTime', event['start'].get('date'))
            comingEvent_end = event['end'].get('dateTime', event['end'].get('date'))

            comingTime_start  = int(comingEvent_start[11] + comingEvent_start[12])
            comingTime_end = int(comingEvent_end[11] + comingEvent_end[12])
            comingDay   = int(comingEvent_start[8] + comingEvent_start[9])
            
            givenTime = int(startTime[11] + startTime[12])
            givenDay = int(startTime[8] + startTime[9])

            if ((comingDay == givenDay) and (givenTime <= comingTime_end and givenTime >= comingEvent_start)):
                return True
           # print(comingEvent_start, event['summary'])
            if (comingDay > givenDay):
                return False
            if (comingTime_start >= (givenTime + 3)):
                return False
            else:
                return True

# more specified to our problem ( should be reliable enough)
def calendar_is_conflict_v2(calendar_service, startTime,endTime):
    eventsResult = calendar_service.events().list(
        calendarId='pfua0o0tbak5vhcbjlq5vqbe50@group.calendar.google.com', timeMin=startTime, timeMax=endTime, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        return False
    else:
        return True

def calender_get_teamIDs(calendar_service,reservedDay_start,reservedDay_end):
    eventsResult = calendar_service.events().list(
        calendarId='pfua0o0tbak5vhcbjlq5vqbe50@group.calendar.google.com', timeMin=reservedDay_start, timeMax=reservedDay_end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        return []
    else:
        return events


# reservedDay format: 'xxxx-xx-xxT00:00:00+02:00'
# return 1 => in case teamID has already a reservation for this today of startDate
# return 2 => in case teamID has already a reservation for the day before of startDate
# return 3 => in case teamID has has already a reservation for the day after of startDate
# return 0 => it's fine
def calendar_is_team_have_successive_requests(calendar_service, startDate, teamID):
    currentDay_start = startDate[0:11] + '01:00:00+02:00'
    currentDay_end = startDate[0:11] + '23:00:00+02:00'

    # a handle like this should be done for month 7 for prevDay
    print(startDate)
    if (startDate[8] + startDate[9] == '30'):
        nextDay = '01'
        nextMonth = str(int(startDate[5] + startDate[6]) + 1)
        nextDay_start = startDate[0:5] +'0'+ nextMonth+'-' + nextDay + 'T' + '01:00:00+02:00'
        nextDay_end = startDate[0:5]   +'0'+nextMonth +'-'+ nextDay + 'T' + '23:00:00+02:00'
    else:
        nextDay = str(int(startDate[8] + startDate[9]) + 1)
        nextDay = sheets_modify_team_ID(nextDay)    # silly -_- regardless the name,it does the job
        nextDay_start = startDate[0:8] + nextDay[0] + nextDay[1] + 'T' + '01:00:00+02:00'
        nextDay_end = startDate[0:8] + nextDay[0] + nextDay[1] + 'T' + '23:00:00+02:00'

    if (startDate[8] + startDate[9] == '01'):
        prevDay = '30'
        prevMonth = str(int(startDate[5] + startDate[6]) - 1)
        prevDay_start = startDate[0:5] +'0'+ prevMonth+'-' + prevDay + 'T' + '01:00:00+02:00'
        prevDay_end = startDate[0:5]   +'0'+prevMonth +'-'+ prevDay + 'T' + '23:00:00+02:00'
    else:
        prevDay = str(int(startDate[8] + startDate[9]) - 1)
        prevDay  = sheets_modify_team_ID(prevDay)
        prevDay_start = startDate[0:8] + prevDay[0] + prevDay[1] + 'T' + '01:00:00+02:00'
        prevDay_end = startDate[0:8] + prevDay[0] + prevDay[1] + 'T' + '23:00:00+02:00'


    current_IDs = calender_get_teamIDs(calendar_service, currentDay_start, currentDay_end)
    prev_IDs = calender_get_teamIDs(calendar_service, prevDay_start, prevDay_end)
    next_IDs = calender_get_teamIDs(calendar_service, nextDay_start, nextDay_end)



    # for id in current_IDs:
    #     print("current:",id['summary'][5:7])
    #
    # for id in prev_IDs:
    #     print("prev:",id['summary'][5:7])
    #
    # for id in next_IDs:
    #     print("next:",id['summary'][5:7])

    reserved = False
    for id in current_IDs:
        if(id['summary'][5:7] == teamID): # already reserved for this day
            reserved = True
    if (reserved == True): return 1

    if not prev_IDs and not next_IDs:
        return 0 # all free so you can reserve

    reserved = False
    for id in prev_IDs:
        if(id['summary'][5:7] == teamID): # already reserved for before this day
            reserved = True
    if (reserved == True): return 2

    if not next_IDs:
        return 0  # all free

    reserved = False
    for id in next_IDs:
        if(id['summary'][5:7] == teamID): # already reserved for after this day
            reserved = True
    if (reserved == True): return 3

    return 0  # you passed all the conditions, so it's valid reservation
