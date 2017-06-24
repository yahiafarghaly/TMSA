# TMSA (Time Management Server Application)

TMSA is a server application which talks to a google spreadsheet and take information from it and reserve an event on google calendar upon this information, Also it send email to the reserver. 

TMSA is created for undergraduate students(teams) to organize their access on a remote server where they train Machine learning models.

  - The spreadsheet form is like [this]( https://goo.gl/forms/hHq2GHUA1w8WFjdI2 )
  - The logic in the script was to ensure that one team can reserve only one time slot within two **successive days**.
  - The python script is using google APIs of sheets,gmail and calendar.