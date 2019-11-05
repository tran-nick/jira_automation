#! python3

from jira import JIRA
import datetime 
from datetime import timedelta
from dateutil.parser import parse
import openpyxl

options = {'server':'ENTER WEBSITE'}
jira = JIRA(options, basic_auth=('USERNAME','PASSWORD'))

ticket = input("Enter ticket number: ")

issue = jira.issue(ticket,expand = 'changelog')
changelog = issue.changelog

#-----------------
""" EXAMPLE
https://community.atlassian.com/t5/Jira-questions/
Is-it-possible-to-get-the-issue-history-using-the-REST-API/qaq-p/510094

for history in changelog.histories:
    for item in history.items:
        if item.field == 'status':
            print( 'Date:' + history.created + ' From:' + item.fromString + ' To:' + item.toString)
"""
#-----------------
#return array of status transactions
def status_change_array(issue_passed, changelog_passed):


    time_array = []

    firstStatus = 'Created'
    createdDate = issue_passed.fields.created
    time_array.append((createdDate, firstStatus, "On Assembly Line"))
    
    for history in changelog_passed.histories:
        for item in history.items:
            if item.field == 'status':
               time_array.append((history.created,item.fromString,item.toString))
    
    return time_array

test = status_change_array(issue,changelog)

for line in test:
    print (line)
    
print()
print("Issue: " + issue.key + " " + issue.fields.summary)
print()

#----------------------
#create array of time calculations
def duration_array(array_passed):

    duration_calc = []
    time = 0
    status = 2
    
    for transition in range(len(array_passed)-1):
        
        fromTime = parse(array_passed[transition][time], ignoretz = True)
        toTime = parse(array_passed[transition+1][time], ignoretz = True)
        delta = toTime - fromTime
        status_time_spent_in = array_passed[transition][status]
        duration_calc.append((status_time_spent_in,delta))
        
        #add duration from last status to now
        now = datetime.datetime.now()
        lastTime = parse(array_passed[len(array_passed)-1][time], ignoretz = True)
        #now_delta = now - lastTime
        #duration_calc.append(now_delta)

    return duration_calc


transition_duration_array = duration_array(test)

for line in transition_duration_array:
    print(line)
print()
comment = ""
for line in transition_duration_array:
    comment += "Time in " + line[0] + " was (days, Hours:Min:Sec) = " + str(line[1]) + "\n"

print(comment)

jira.add_comment(ticket, comment)
print("Comment was added")
