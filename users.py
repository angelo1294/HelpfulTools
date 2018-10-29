import json
import requests
import ast

def createUsers(session,url, data, headers, auth):
	return session.post(url,data=data,headers=headers, auth=auth)

#Hosts settings
domainName = '.spirenteng.com'
ite = 'ite-agrama-latest'
velocity = 'vel-agrama-latest'
failList = []

#Rest settings for ITE
protocol = 'https://'
url = protocol + ite + domainName + '/useradm'
credentials = {'user':'root', 'passw':'admin', 'userid':'spirent','name':'spirent','password':'spirent'}
headers = {'Content-Type':'application/x-www-form-urlencoded'}
auth = (credentials['user'], credentials['passw'])
session = requests.Session()

#Create body
for i in range(1, 20):
	data = 'mode=update&userid=%s&name=%s&password=%s' % (credentials['userid']+str(i), credentials['name']+str(i), credentials['password']+str(i))
	output = session.post(url,data=data,headers=headers, auth=auth)
	if '200' in str(output):
		pass
	else:
		failList.append(credentials['userid']+str(i))
		continue


if failList:
	print("Failed to create users: " + str(failList))