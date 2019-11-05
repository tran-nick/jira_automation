#! python3

from jira import JIRA
import openpyxl
from openpyxl import Workbook


##authenticate instance
options = {'server':' ENTER WEBSITE '}
jira = JIRA(options, basic_auth=('USERNAME','PASSWORD'))



#Calling excel sheet
serial_list = "Book1.xlsx"

wb = openpyxl.load_workbook(serial_list)
ws = wb.active

colA = ws['A']

#check column
"""for serial in colA:
    print(serial.value)
    print()
"""


#index variable for iterating
row = 1

for serial in colA:

    col = 2

    print(serial.value)
        
    try:
        query = jira.search_issues("project = NCM AND \
    issuetype = module AND summary ~" + serial.value)

        if len(query) == 1:
            NCM_key = jira.issue(query[0].key)

    except:
        print("There was more than 1 matching issue.")

    NCM_ticket = jira.issue(NCM_key)
    subtasks = NCM_ticket.fields.subtasks


    #take subtasks resource and search for applicable subtask in parent ticket
    for issue in subtasks:
        
        if "State of Charge" in issue.fields.summary:
            SOC_subtask = issue.key

            comments = jira.comments(issue.key)

            print(issue.key)
            print()

            for string in comments:
                ws.cell(row , col , value = string.body)
                #move to next column
                col+=1

            row+=1 

wb.save(serial_list)
