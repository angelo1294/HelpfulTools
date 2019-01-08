import yaml
import argparse
import atexit
import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import collections
from veloRequests import *

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
######Arguments parser##############
parser = argparse.ArgumentParser(description=
	"""Get input_json from a reserved topology in Velocity""")

######Argument List###################
parser.add_argument('-velocity', help="Velocity in use", type=str)
parser.add_argument('-username', help="User Id for Velocity login", type=str)
parser.add_argument('-password', help="Password for Velocity login", type=str)
parser.add_argument('-VELOCITY_PARAM_RESERVATION_ID', help="Id of the reservation", type=str)
args = parser.parse_args()


if __name__ == '__main__':
	build = {}
	velo = 'vel-agrama-latest.spirenteng.com'
	username = 'spirent'
	password = 'spirent'
	# reservationId = 'b0c5b7dc-0226-4ad0-b3fe-a3c19019d316'
	reservationId = '81775b3e-1d22-45ec-aa67-2b80ff94bca2'
	
	data = getTopology(args.velo, args.username, args.password, args.VELOCITY_PARAM_RESERVATION_ID)
	topologyName = data['topology_template']['node_templates']['topology']['properties']['name']
	
	'''Get Devices ids for each subnet'''
	build.update(createZoneBody(data, build))
	
	'''Get names of devices'''
	# for zone in build:		
	# 	build[zone].update(getDeviceNames(data, build[zone]))
	build.update(getDeviceNames(data, build))

	'''Get ports of devices'''
	for zone in build:
		build[zone].update(getDevicePorts(data, build[zone], velo, username, password))
	
	body = createJsonBody(build, topologyName)
	# createJsonBody(build, topologyName)
	print(body)
	# print(build)		