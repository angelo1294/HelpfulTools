import json
from concurrent.futures import ThreadPoolExecutor
import requests
import ast

def postReservation(url, data):
	return session.post(url,data=data)

def buildDuplicates(body, duplicateElement, nrOfDuplicates, dictOfElements=""):
	bodyList = []
	data = json.loads(body)
	newData =json.loads(body)
	for i in range(0,nrOfDuplicates):
		newData[duplicateElement] = data[duplicateElement] + str(i)
		if dictOfElements:
			for key in dictOfElements:
				for value in dictOfElements[key]:
					 newData[key] = value
		tmp = json.dumps(ast.literal_eval(str(newData)))
		bodyList.append(str(tmp))
	return bodyList

#Set variables and raw body data
topologyIdList = ['5fad0453-8052-4bef-97be-b714bebbd230','3ebb1742-39ae-4517-88e1-bd76eaefc9e2', '64310c86-cc6a-4d00-bae5-b9341eaed862', 'bbf0cef1-9c1e-4c72-a0ce-d8970322606c', '30595b30-1225-4dd9-bffd-825b82419199']
urlPostReservation = 'https://vel-3601-agrama.spirenteng.com/velocity/api/reservation/v10/reservation?ignoreVlanConflicts=false'
body = '{ "name": "Agrama simultaneous reservation", "start": null, "duration": 600, "topologyId": "", "isRecurrent": false, "escalationRequest": null }'
jsonDict = {'topologyId':topologyIdList}
#Create session
session = requests.Session()
session.auth = ("spirent","spirent")

#Create list with bodies
#print(jsonDict)
bodyList = buildDuplicates(body, 'name', 5)
# for top,i in zip(topologyIdList,range(1,6)):
# 	data['name'] = name + str(i)
# 	data['topologyId'] = top
# 	tmp = json.dumps(ast.literal_eval(str(data)))
# 	bodyList.append(tmp)
print(bodyList)

#Send simultaneous Post requests
# with ThreadPoolExecutor(max_workers=50) as executor:
# 	task1 = executor.submit(postReservation(urlPost,bodyList[0]),'task1')
# 	task2 = executor.submit(postReservation(urlPost,bodyList[1]),'task2')
# 	task3 = executor.submit(postReservation(urlPost,bodyList[2]),'task3')
# 	task4 = executor.submit(postReservation(urlPost,bodyList[3]),'task4')
# 	task5 = executor.submit(postReservation(urlPost,bodyList[4]),'task5')