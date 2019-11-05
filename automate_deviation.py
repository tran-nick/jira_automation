#! python3

from jira import JIRA
import openpyxl
from openpyxl import Workbook
import os

#authenticate instance
#----------------------------
options = {'server':'https:// ENTER WEBSITE HERE'}
jira = JIRA(options, basic_auth=('USERNAME','PASSWORD'))
#----------------------------


get_deviation = input("Enter Deviation ticket number: ")
deviation = jira.issue(get_deviation)

#read excel to create issue array
#----------------------------
ncm_list = 'Book1.xlsx'

wb = openpyxl.load_workbook(ncm_list)

#active first sheet by default
ws = wb.active

issue_array = []
del issue_array[:]

colA = ws['A']
for row in colA:
    print(row)
    if row != None:
        issue_array.append(row.value)
print(issue_array)
print("")
print(len(issue_array))
print("")
#----------------------------

#Update shouldbe for all tickets
#----------------------------
def shouldbe_update(issue_array):
    print("Updating Should Be Field\n")
    
    should_be = """
1: Should be requirement 1
2: Should be requirement 2
3: Should be requirement 3
4: Should be requirement 4
5: Should be requirement 5
6: Should be requirement 6
7: Should be requirement 7
8: Should be requirement 8
"""
    for serial_number in issue_array:
        search = jira.search_issues("project = NCM AND issuetype = module AND summary ~" + serial_number)

        print(search)

        if len(search) ==1:
            ticket = jira.issue(search[0].key)
            ticket.update(fields={'customfield_12233':should_be})
            print(serial_number + " should_be update TRUE")


#----------------------------
#----------------------------
#iterate through array of NCM string to link to deviation ticket
#----------------------------
def deviation_link(issue_array):

    for serial_number in issue_array:
        search = jira.search_issues("project = NCM AND issuetype = module AND summary ~" + serial_number)
        print(search)
        
        if len(search) ==1:
            ticket = jira.issue(search[0].key)
            jira.create_issue_link(
                type = "is approved by",
                #need to pass issue key as string
                inwardIssue = search[0].key,
                outwardIssue = deviation.key)
            print("linked " + search[0].key + " TRUE")
#----------------------------
#----------------------------
#----------------------------
#----------------------------
def labels_by_serialNumber(issue_array):
    print("Updating ticket with label for query")
    print("")

    newLabel = input("Label to add:")

    for NCM in issue_array:
        print(NCM)
        search = jira.search_issues("project = NCM AND issuetype = module AND summary ~" + NCM)
        print(search)

        if len(search) ==1:
            issue = jira.issue(search[0].key)
            issue.fields.labels.append(newLabel)
            issue.update(fields = {"labels":issue.fields.labels})
            print("label updated TRUE")
            print("")
        

    print("Label Update Done")
    print("")
#----------------------------


    

#RUN CODE
labels_by_serialNumber(issue_array)
shouldbe_update(issue_array)
deviation_link(issue_array)
print("Success")
