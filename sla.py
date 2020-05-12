#!/bin/python
import sys
from jira import JIRA
#from pass1 import pass1
import urllib3
import pandas as pd
import csv
from datetime import date,datetime
from datetime import timedelta


def converttime(resolutiontime):
 #Define the constants
 SECONDS_PER_MINUTE  = 60
 SECONDS_PER_HOUR    = 3600
 SECONDS_PER_DAY     = 86400
 #total_seconds = 0
 
 if "days" in resolutiontime:
   
   days=resolutiontime.split()[0]
   hours=resolutiontime.split(",")[1].split(":")[0]
   minutes=resolutiontime.split(",")[1].split(":")[1]
   seconds=resolutiontime.split(",")[1].split(":")[2]
 else:
   days=0
   hours=resolutiontime.split(":")[0]
   minutes=resolutiontime.split(":")[1]
   seconds=resolutiontime.split(":")[2]
   
 total_seconds = days * SECONDS_PER_DAY
 print (total_seconds ,hours ,SECONDS_PER_HOUR)
 total_seconds = total_seconds + ( hours * SECONDS_PER_HOUR)
 total_seconds = total_seconds + ( minutes * SECONDS_PER_MINUTE)
 total_seconds = total_seconds + seconds
 
 #print (total_seconds)
 
 return total_seconds

urllib3.disable_warnings()

## Credentials passed 
#username=str(sys.argv[1]) 
username="<>"
pass1="<>" 
month="02"

##List of vars
first=0
second=0
third=0
p1={}
p2={}
p3={}
ticket_status={}
list_cat= set()
list_status= set()
#if not month:
#	today = date.today()
#	month=today.month
now=datetime.now()
date=now.strftime("%Y%m%d%H%M%S")
outputFile="SLA_"+date+".xlsx"

print ("Output File :",outputFile,month)

sit=["abc, xyz"]
labels=["Second_Line_Support"]

##Jira API to make connection
jira = JIRA(options={'server':'https://jira.xyz.com/'}, basic_auth=(username,pass1))


issues = jira.search_issues("project = DASSIST AND assignee in (chetan.sharma,anurag.gulati,mayank.Batra,prabhat.singh) AND issuetype = Support AND created >= 2020-"+str(month)+"-01 AND created <= 2020-"+str(month)+"-29 ORDER BY createdDate ASC " ,maxResults=5000)

#print (issues)

status1="Closed"
##Logic to parse tickets basis of category
for tickets in issues:
        
        #print (tickets)
        status=tickets.fields.status
        #print (jira.transitions(tickets,"status"))
        #sys.exit()
        
        if str(status) in status1:
           priority=str(tickets.fields.priority)
           created=tickets.fields.created
           resolved=tickets.fields.resolutiondate
           createdTime = datetime.strptime(created[:19], '%Y-%m-%dT%H:%M:%S')
           resolvedTime = datetime.strptime(resolved[:19], '%Y-%m-%dT%H:%M:%S')
           #print ("Created "+ str(created) + " Resolved "+ str(resolved))
           resolution_time=resolvedTime-createdTime
           #resolution_time=(resolution_time.total_seconds() / 3600)
           #print ("resolution"+ str(resolution_time))
           #resolution_time=converttime(str(resolution))
           if priority == "Critical":  
             p1[str(tickets)]=resolution_time
           elif priority == "Important":
             p2[str(tickets)]=resolution_time
           elif priority == "Normal":
             p3[str(tickets)]=resolution_time

			 
timedeltas_p1=[]
timedeltas_p2=[]
timedeltas_p3=[]
fieldnames = ['Priority','Ticket', 'Time Taken[Hours]', 'Average[Hours]']
	 
with open(outputFile, 'a') as csvfile:
   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
   writer.writeheader()
	 
## Printing Output
for key,val in p1.items():
  print ("P1 : ", key, "=>", round(val.total_seconds() / 3600 ,1))
  timedeltas_p1.append(val)
  with open(outputFile, 'a') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writerows([{'Priority': 'P1','Ticket': key , 'Time Taken': round(val.total_seconds() / 3600 ,1)}])
	 
average_timedelta_p1_1 = sum(timedeltas_p1, timedelta(0)) / len(timedeltas_p1)
average_timedelta_p1=round(average_timedelta_p1_1.total_seconds() / 3600 , 1)

with open(outputFile, 'a') as csvfile:
   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
   print (average_timedelta_p1)
   writer.writerows([{'Priority': 'AVERAGE','Average': average_timedelta_p1}])
  
print ("#########################")

for key,val in p2.items():
  print ("P2 : ", key, "=>", round(val.total_seconds() / 3600 ,1))
  timedeltas_p2.append(val)
  with open(outputFile, 'a') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writerows([{'Priority': 'P2','Ticket': key , 'Time Taken': round(val.total_seconds() / 3600 ,1)}])
	 
average_timedelta_p2 = sum(timedeltas_p2, timedelta(0)) / len(timedeltas_p2)
print (average_timedelta_p2)

with open(outputFile, 'a') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writerows([{'Priority': 'AVERAGE','Average': average_timedelta_p2[:8]}])

print ("#########################")

for key,val in p3.items():
  print ("P3 : ", key, "=>", round(val.total_seconds() / 3600 ,1))
  timedeltas_p3.append(val)
  with open(outputFile, 'a') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writerows([{'Priority': 'P3','Ticket': key , 'Time Taken': round(val.total_seconds() / 3600 ,1)}])
	 
average_timedelta_p3 = sum(timedeltas_p3, timedelta(0)) / len(timedeltas_p3)
print (average_timedelta_p3)
  
with open(outputFile, 'a') as csvfile:
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writerows([{'Priority': 'AVERAGE','Average[Hours]': average_timedelta_p3}])

"""

## Printing Output
for key,val in first_dict.items():
        print ("First Level : ", key, "=>", val)
        first=first+val
print ("Total First line: ", first)

for key1,val1 in second_dict.items():
        print ("Second Level : ", key1, "=>", val1)
        second=second+val1
print ("Total second line : ",second)

## Printing Status
for key,val2 in ticket_status.items():
        print ( key, "=>", val2)
        third=third+val2
		
#denominator=first+second+third
denominator=second+third


fieldnames = ['Ticket Category', 'Resolved By 1st Line','Resolved By 2nd Line','Gross Tickets']
with open(outputFile, 'a') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	

for items in list_cat:
        with open(outputFile, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if items not in first_dict.keys():
                first_dict[items]=""
            if items not in second_dict.keys():
                second_dict[items]=""
            writer.writerows([{'Ticket Category': items , 'Resolved By 1st Line': first_dict[items] , 'Resolved By 2nd Line': second_dict[items] }])
			
with open(outputFile, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows([{'Ticket Category': "Total" , 'Resolved By 1st Line': first , 'Resolved By 2nd Line': second, 'Gross Tickets':denominator}])
	
##calculation
ResolveFirstPer=first/denominator*100
ResolveSecondPer=second/denominator*100

	
with open(outputFile, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows([{'Ticket Category': "Percentage" , 'Resolved By 1st Line': ResolveFirstPer , 'Resolved By 2nd Line': ResolveSecondPer}])
	

for items in list_status:
        with open(outputFile, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #if items not in first_dict.keys():
            #    first_dict[items]=""
            #if items not in second_dict.keys():
            #    second_dict[items]=""
            writer.writerows([{'Ticket Category':items , 'Resolved By 1st Line': ticket_status[items] }])


#print "Bitbucket :1st level- "+str(first)+" | 2nd level- "+str(second)



#df = pd.DataFrame(issues)
#df.to_csv('Output.csv')
"""
