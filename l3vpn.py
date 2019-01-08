import yaml
import argparse
import atexit
import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import collections

###############################################
###Get YAML format of topology from Velocity###
###############################################
def getTopology(velo, user, password, reservationId):
	url = 'https://' + velo + '/velocity/api/reservation/v11/reservation/' + reservationId + '/topology'
	rq = requests.get(url, verify=False, auth=(user, password),
                          headers={'Accept': 'application/vnd.spirent-velocity.topology.tosca+yaml'})
	return yaml.load(rq.text)

#########################################
###Get subnets from YAML and create body#
#########################################
def createZoneBody(data,build):
####Parse subtopologies and select zone name and id
	for subtopology in data['topology_template']['groups']:
		if ('Zone' in data['topology_template']['groups'][subtopology]['properties']['name']) or ('zone' in data['topology_template']['groups'][subtopology]['properties']['name']):
			zone = data['topology_template']['groups'][subtopology]['properties']['name']
			build[zone] = {}
			build[zone]['id']= data['topology_template']['groups'][subtopology]['properties']['id']
####Parse subtopologies, select subnets and insert into zone
	for subtopology in data['topology_template']['groups']:
		if ('subnet' in data['topology_template']['groups'][subtopology]['properties']['name']):
			for zone in build:
				if build[zone]['id'] in subtopology:
					subnet = data['topology_template']['groups'][subtopology]['properties']['name']
					build[zone][subnet] = {}
					for element in data['topology_template']['groups'][subtopology]['members']:
						if 'device' in element:
							build[zone][subnet][element] ={}
####Delete id key-element
	for zone in build:
		del build[zone]['id']
	return build

##################################################################
###Using portId of the device, get the groupName from Inventory###
##################################################################
def getPortGroupName(velo, user, password, deviceId, portId):
	portUrl = 'https://' + velo + '/velocity/api/inventory/v8/device/' + deviceId + '/port/' + portId
	rq = requests.get(portUrl, verify=False, auth=(user, password))
	if 'errorId' in rq.text:
		print('Error retrieving information about the device(' + deviceId +') port(' + portId + '). Message: ' + result['message'])
	else:
		portGroupUrl = 'https://' + velo + '/velocity/api/inventory/v8/device/' + deviceId + '/port_group/' + json.loads(rq.text)['groupId']
		rq = requests.get(portGroupUrl, verify=False, auth=(user, password))
	if 'errorId' in rq.text:
		print('Error retrieving information about the device(' + deviceId +') port group. Message' + result['message'])
		return ''	
	else:
		return json.loads(rq.text)['name']

############################################################################################
###Search in YAMl the vlan_link that contains our port id and use the vlanId to get vlan_id#
############################################################################################
def getVlanIdFromYaml(data, portId):
	vlanId = ''
	for vlanLink in data['topology_template']['node_templates']:
		if 'vlan_link' in vlanLink:
			if data['topology_template']['node_templates'][vlanLink]['requirements'][0]['from'] == portId:
				topoVlan = data['topology_template']['node_templates'][vlanLink]['requirements'][1]['to']
				vlanId = data['topology_template']['node_templates'][topoVlan]['properties']['vlan_id']
				break
			elif data['topology_template']['node_templates'][vlanLink]['requirements'][1]['to'] == portId:
				topoVlan = data['topology_template']['node_templates'][vlanLink]['requirements'][0]['from']
				vlanId = data['topology_template']['node_templates'][topoVlan]['properties']['vlan_id']
				break
	return vlanId

#####################################
###Get device names and properties###
#####################################
def getDeviceNames(data, build):
	for element in data['topology_template']['node_templates']:
		for zone in build:
			for subnet in build[zone]:
				if element in build[zone][subnet]:
					build[zone][subnet][element]['name'] = data['topology_template']['node_templates'][element]['properties']['name']
					build[zone][subnet][element]['inventory_id'] = data['topology_template']['node_templates'][element]['properties']['inventory_id'] 
					for property_group in data['topology_template']['node_templates'][element]['properties']['property_groups']:
						if 'System Identification' == property_group['name']:
							for group in  property_group['group']:
								if group['name'] == 'ipAddress':
									build[zone][subnet][element]['mgmt_ip'] = group['value']
									build[zone][subnet][element]['ports'] = []  ###Move this line and the next to the next if when uncomenting the last 2 lines
									continue
							# 	if group['name'] == 'type':
							# 		build[zone][subnet][element]['type'] = group['value']
	return build

#################################################
###Get ports of devices and populate properties##
#################################################
def getDevicePorts(data, build, velo, username, password):
	for element in data['topology_template']['node_templates']:
		if 'port' in element:
			for subnet in build:
				for device in build[subnet]:
					if device == data['topology_template']['node_templates'][element]['requirements'][0]['device']:
						port = {}
						port['nameId'] = element
						port['name'] = data['topology_template']['node_templates'][element]['properties']['name']
						port['inventory_id'] = data['topology_template']['node_templates'][element]['properties']['inventory_id']
						port['id'] = data['topology_template']['node_templates'][element]['properties']['id']
						'''Get Vlan id of port'''
						port['vlan_id'] = getVlanIdFromYaml(data, port['nameId'])
						port['vlan_type'] = getPortGroupName(velo, username, password, build[subnet][device]['inventory_id'], port['inventory_id'] )
						build[subnet][device]['ports'].append(port)
	return build

def createJsonBody(build, topologyName):
	domain = {'name': topologyName, 'domain':{'zones':[]}}
	for zoneName in build:
		zone = {'name':zoneName, 'subnets':[]}
		for subnetName in build[zoneName]:
			subnet = {'name': subnetName, 'devices':[]}
			for deviceId in build[zoneName][subnetName]:
				device = {}
				device['name'] = build[zoneName][subnetName][deviceId]['name']
				device['mgmt_ip'] = build[zoneName][subnetName][deviceId]['mgmt_ip']
				device['bootstrap'] = ''
				if 'nsg' in device['name'] or 'nsg'.upper() in device['name']:
					device['type'] = 'nsg'
				else:
					device['type'] = 'client'
				device['ports'] = []
				for usedPort in build[zoneName][subnetName][deviceId]['ports']:
					port = {}
					port['physical_port'] = usedPort['name']
					port['type'] = usedPort['vlan_type']
					if usedPort['vlan_id']:
						port['lan_id'] = usedPort['vlan_id']
					port['mac_address'] = 'to be generated'
					device['ports'].append(port)
				subnet['devices'].append(device)
			zone['subnets'].append(subnet)
		domain['domain']['zones'].append(zone)
	return json.dumps(domain)			


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
######Arguments parser##############
parser = argparse.ArgumentParser(description=
	"""Get input_json from a reserved topology in Velocity""")

######Argument List###################
parser.add_argument('-velo', help="Velocity to connect", type=int)
parser.add_argument('-username', help="User Id to login into Velocity", type=int)
parser.add_argument('-password', help="Password of the user to login into Velocity", type=int)
parser.add_argument('-reservationID', help="Id of the current reservation", type=int)
args = parser.parse_args()


if __name__ == '__main__':
	build = {}
	velo = 'vel-agrama-latest.spirenteng.com'
	username = 'spirent'
	password = 'spirent'
	# reservationId = 'b0c5b7dc-0226-4ad0-b3fe-a3c19019d316'
	reservationId = '81775b3e-1d22-45ec-aa67-2b80ff94bca2'
	
	data = getTopology(velo, username, password,reservationId)
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