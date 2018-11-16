import argparse
import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

######################################
######Required Variables##############
######################################
'''MUST BE SET BEFOREHAND '''
######################################
velocityList = ['vel-agrama-latest']
iteList = ['ite-agrama-latest']
version = '7.2.0'

######################################
###Parse arguments passed to script###
######################################
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
parser = argparse.ArgumentParser(description=
								"""IMPORTANT NOTE: Set the required variables at the begining of the 
								script(such as version and VM list) before execution...
								Program receives the server address along with credentials and 
								updates the build of your VM list.""")

######Argument List###################
parser.add_argument('-server', help="vSphere server to point to", type=str)
parser.add_argument('-user', help="Username for vSphere server", type=str)
parser.add_argument('-passw', help="Password for vSphere server", type=str)
args = parser.parse_args()

#####Beggining of methods#############
def authenticateToServer(server, user, passw):
	url = 'https://'+ server +  '/rest/com/vmware/cis/session'
	rq = requests.post( url, verify=False, auth=(user, passw))
	response = json.loads(rq.text)
	return response['value']

# if isinstance(produc, list):
# 		for vm in product
# 	else:


def getLastBuild(token, version, product, server):
	##########Get vmid of Virtual machine############
	url = 'https://' + server + '/rest/vcenter/vm?filter.names.1=' + product
	rq = requests.get(url,  verify=False, headers={'vmware-api-session-id': token})
	response = json.loads(rq.text)
	##########Get Virtual machine information########
	url = 'https://' + server + '/rest/vcenter/vm/' + response['value'][0]['vm']
	rq = requests.get(url,  verify=False, headers={'vmware-api-session-id': token})
	response = json.loads(rq.text)
	print(response)
#token = authenticateToServer(args.server, args.user, args.passw)
#getLastBuild(token, '7.2.0', 'vel-agrama-latest', args.server)