#! python3

from jira import JIRA

#authenticate instance
#----------------------------
options = {'server':'ENTER WEBSITE HERE'}
jira = JIRA(options, basic_auth=('USERNAME','PASSWORD'))
#----------------------------


def batchMode():

    update_array = []
    
    print("")
    print("BATCH MODE IS ON. Continue scanning serial numbers \n")
    
    while True:
        serial_number = input("SCAN SERIAL NUMBER:")

        if len(serial_number)!= 7:
            print("Input length was " + str(len(serial_number)) + ". Not recognized as a serial number.")
            print("")
            break

        elif len(serial_number)== 7:

            update_array.append(serial_number)
            

    #Exiting while loop------------------
    print("BATCH MODE IS OFF")
    if len(update_array)== 0:
        print("No serial numbers received. Nothing was done\n")

    elif len(update_array)> 0:
        print(update_array)
    
        update2 = input("SCAN BATCH UPDATE ITEM LOCATION:")

        for module in update_array:
            search2 = jira.search_issues("project = NCM AND issuetype = module AND summary ~" + module)
            print(search2)
            if len(search2) == 1:
                issue = jira.issue(search2[0].key)
                issue.update(fields={'customfield_10723':update2})
                print("Updated Success!\n")
            
           
            
#--------------------------------        
    

while True:
    print("Enter \"quit\" to close program\n")
    print("Enter \"batch\" to start batch update\n")
    serial_number = input("SCAN SERIAL NUMBER:")
    search = jira.search_issues("project = NCM AND issuetype = module AND summary ~" + serial_number)

    if len(search)==1:
        
        issue = jira.issue(search[0].key)

        update = input("SCAN ITEM LOCATION:")
        issue.update(fields={'customfield_10723':update})
        print("Updated!\n")

    elif len(search) > 1:
        print("Multiple reslults found!")
        for result in search:
            print(result.key + " " + result.fields.summary)

    elif serial_number.upper() == "QUIT":
      break

    elif serial_number.upper() == "BATCH":
        batchMode()
        
                

        
print("")
print("Program is closing")
print("Goodbye!")
