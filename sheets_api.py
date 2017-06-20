
# spreadsheetId is unique for every created spread sheet
spreadsheetId = '1C4k7Vb7Jl5grSrhUf6x600B82U7P16QtwVqxUjs1I-A' # for our sheet
sheetId = 947337044

# Author:           Yahia Farghaly (yahiafarghaly@outlook.com)
# Return: rows_values[0] .. rows_values[4]
# Usage Example:
    # values = retrieve_first_row(sheets_service)
    # if not values:
    #     print('No data found.')
    # else:
    #     for row in values:
    #         print('%s, %s, %s, %s, %s,%s' % (row[0], row[1], row[2], row[3], row[4],row[5]))
def retrieve_first_row(sheets_service):
    #rangeName is based on a1-notation,for more: https://developers.google.com/sheets/api/guides/concepts#a1_notation
    rangeName = 'ServerSheet!B2:G2' # 2 not 1 due to the title of each cell
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    row_values = result.get('values', [])
    return row_values



def delete_first_row(sheets_service):
    batch_update_spreadsheet_request_body = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": sheetId,
                        "dimension": "ROWS",
                        "startIndex": 1,
                        "endIndex": 2
                    }
                }
            },
        ],
    }
    request = sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=batch_update_spreadsheet_request_body)
    response = request.execute()
    return response


def convert_date_to_iso_format(date,time):
    startTime, endTime = convert_time_range_24_format(time)
    # 2017-06-20T


    daybefore = date[6] + date[7] + date[8] + date[9] + '-' + date[3] + date[4] + '-' + date[0] + date[1] + 'T'

    if (endTime == '00:45:00+02:00'): # bad case resulted from wrong choosing of time start, in 24 hr system you should start with AM first not PM
        nextDay = str(int(date[0] + date[1]) + 1)
        dayAfter = date[6] + date[7] + date[8] + date[9] + '-' + date[3] + date[4] + '-' + nextDay[0] + nextDay[1] + 'T'
    else:
        dayAfter = daybefore

    startDate = daybefore + startTime
    endDate = dayAfter + endTime

    return startDate,endDate

def convert_time_range_24_format(time):
    startTime = '00'
    endTime = '00'
    if (time == '12:00 PM to 3:00 PM'):
        startTime = '12:00:00+02:00'
        endTime   = '15:00:00+02:00'

    elif (time == '3:15 PM to 6:15 PM'):
        startTime = '15:15:00+02:00'
        endTime   = '18:15:00+02:00'

    elif (time == '6:30 PM to 9:30 PM'):
        startTime = '18:30:00+02:00'
        endTime   = '21:30:00+02:00'

    elif (time == '9:45 PM to 12:45 AM'):
        startTime = '21:45:00+02:00'
        endTime   = '00:45:00+02:00'

    elif (time == '1:00 AM to 3:00 AM'):
        startTime = '01:00:00+02:00'
        endTime   = '03:00:00+02:00'

    elif (time == '3:15 AM to 5:15 AM'):
        startTime = '03:15:00+02:00'
        endTime   = '05:15:00+02:00'

    elif (time == '5:30 AM to 8:30 AM'):
        startTime = '05:30:00+02:00'
        endTime   = '08:30:00+02:00'

    elif (time == '8:45 AM to 11:45 AM'):
        startTime = '08:45:00+02:00'
        endTime   = '11:45:00+02:00'

    return startTime,endTime

def sheets_modify_team_ID(teamID):
    team_id = int(teamID)
    if(team_id <= 9):
        return '0' + teamID
    else:
        return teamID