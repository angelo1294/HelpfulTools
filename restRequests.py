import requests 
import json, ast
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
############################
######Global Variables######
############################
toDelete = {}              #Dictionary of lists containing elements to delete
vel = "vel-agrama-latest"
vSphereTopologyIdList = ['cd2da007-f9ba-4559-b75b-e7dc5a54db96', '6353b2ba-c602-419f-843e-820487b9d71e', '8e308f2c-779d-4a8e-b41d-d226b1cff36b', '0eefe448-b3ce-4f94-8aaf-e4ec6ba0ff9e', '655340c8-6490-4fd6-a160-8592469ed26e', '5794ec9c-ec9e-4ab6-9f58-09ec84d8362a',
                            '1148d3dd-b922-42b4-a4a5-83962d74a778', 'e346cc72-a737-430d-b832-51b79539d3de', 'e4798915-6a59-4a94-92e7-2c8402c6d582', 'c329dabf-59d5-4a6d-a412-d8a6e62ffe53', '8d440d5f-ad39-4e5a-98ec-c2d52178d3d8', '5ae15b68-3ff1-4d7a-b5e0-5dc1e274a2b8']
openStackTopologyIdList = ['3e665ff3-c7d3-4856-ac48-17e3d01f0ba6', '5da442fc-9ded-49ae-853d-39eadd651799', '7a32335d-2ffa-4c85-9a50-0ed033c97a7d', 'b7343b27-689a-41c6-b481-f19ab77e9b0f', '2307f9bf-4e68-4c4a-8feb-107e174feaca', 
                            '677d17bf-410d-41da-b537-76d1edbad899', 'daa0b20f-f6c2-467d-9b72-8c7877f83783', '84518a20-d7d2-431b-9447-5ddb6b50fdf6', '62c3508a-839b-4daa-9003-36aa45b1a6b1', 'affad43d-6f82-4c81-baa5-e24f806dc2ba']

###############################
##Create vSphere Clouds########
###############################
def createVsphereClouds (velo, qty='', startIndex='', stopIndex=''):
    BaseUrl = "https://"+velo+".spirenteng.com/velocity/api/cloud/v4/cloud"
    if qty and startIndex: 
        stopIndex = qty + startIndex - 1 
    elif qty: 
        startIndex = 1
        stopIndex = qty

    for i in range(startIndex, stopIndex+1):
        body = {}
        body['providerType'] = 'VMWARE'
        body['name'] = 'vSferaindex' + str(i),
        body['description'] = 'vSferaIndex Testing <-> Agrama teritory. Beware of clickbaits'
        body['endpoint'] = 'https://vcenter-apt-dut.spirenteng.com/sdk'
        body['credentials'] = {'username':'agrama@vshphere.local','password':'Agrama123!'}
        body = json.dumps(body)
        rq = requests.post(BaseUrl, data=body, verify=False, auth=('spirent', 'spirent'),
                           headers={'Content-type': 'application/json'})
        print(rq.text)
###############################
##Create OpenStack clouds######
###############################
def createOpenStackClouds (velo, qty='', startIndex='', stopIndex=''):
    BaseUrl = "https://"+velo+".spirenteng.com/velocity/api/cloud/v4/cloud"
    if qty and startIndex: 
        stopIndex = qty + startIndex - 1 
    elif qty: 
        startIndex = 1
        stopIndex = qty

    for i in range(startIndex, stopIndex+1):
        body = {}
        body['providerType'] = 'OPEN_STACK'
        body['name'] = 'OpixStiva' + str(i),
        body['description'] = 'OpixStiva <-> Agrama teritory. Beware of clickbaits'
        body['endpoint'] = 'http://10.140.71.22:5000/v3'
        body['credentials'] = {'username':'admin_gimi','password':'admin_gimi!'}
        body['properties'] = [{'id': 'domain', 'value': 'gimi_test'}, {'id': 'region', 'value': 'RegionOne'}, {'id': 'tenant', 'value': 'admin_gimi'}]
        body = json.dumps(body)
        rq = requests.post(BaseUrl, data=body, verify=False, auth=('spirent', 'spirent'),
                           headers={'Content-type': 'application/json'})
        print(rq.text)
########################################
##Copy published abstract topology######
########################################
def createCopyTopologies (velo, topologyBody, qty='', startIndex='', stopIndex=''):
    initPostUrl = "https://"+velo+".spirenteng.com/velocity/api/topology/v8/topology"
####Post initial topology#####
    rq = requests.post(initPostUrl, data=topologyBody, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/vnd.spirent-velocity.topology.tosca+yaml'})
    initial = json.loads(rq.text)
    if 'errorId' in rq.text:
            print('Topology creation error. Message: ' + initial['message'])
    copyPostUrl = initPostUrl + '?copyFrom=' + initial['id']
    if qty and startIndex: 
        stopIndex = qty + startIndex - 1 
    elif qty: 
        startIndex = 1
        stopIndex = qty
    for i in range(startIndex, stopIndex+1):
        raw = {}
        raw['name'] = 'Rest Performance Topology ' + str(i)
        raw['isAbstract'] = 'true'
        raw = json.dumps(raw)
        rq = requests.post(copyPostUrl, data=raw, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        result = json.loads(rq.text)
        if 'errorId' in rq.text:
            print('Topology copy error. Message: ' + result['message'])
        else:
            toDelete.append(result['id'])
        BaseUrlPUT = "https://"+velo+".spirenteng.com/velocity/api/topology/v8/topology/" + result['id']
        body = {}
        body['isDraft'] = 'false'
        body = json.dumps(body)
        rq = requests.put(BaseUrlPUT, data=body, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        topology = json.loads(rq.text)
        if 'errorId' in rq.text:
            print('Topology publishing error. Message: ' + topology['message'])
####Create reservation########
        postReservationUrl = "https://"+velo+".spirenteng.com/velocity/api/reservation/v11/reservation"
        reservationBody = {}
        reservationBody['name'] = 'Reservation of test Topology ' + str(i)
        reservationBody['duration'] = '300'
        reservationBody['topologyId'] = topology['id']
        reservationBody = json.dumps(reservationBody)
        rq = requests.post(postReservationUrl, data=reservationBody, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        print(rq.text)
###################################################################################################################################
##Create port groups##########Start from a parent device with port group and create devices and port groups linked to this parent##
###################################################################################################################################
def createPortGroups (velo, deviceTemplateId, portTemplateId, groupId, qty='', startIndex='', stopIndex='', portsPerGroup=''):
    devicePostUrl = "https://"+velo+".spirenteng.com/velocity/api/inventory/v8/device"
####Create ports json#################
    if not portsPerGroup:
        portsPerGroup = 5
    portsBody = {}
    portsBody['ports'] = []
    port = {}
    for i in range(1, portsPerGroup+1):
        port['groupId'] = 'Some Id'
        port['name'] = 'Port ' + str(i) 
        port['templateId'] = portTemplateId
        portsBody['ports'].append(port.copy())
####Index management##########################
    if qty and startIndex: 
        stopIndex = qty + startIndex - 1 
    elif qty: 
        startIndex = 1
        stopIndex = qty
    for i in range(startIndex, stopIndex+1):
########Device handling######################
        deviceBody = {}
        deviceBody['name'] = 'Performance Port Group Test ' + str(i)
        deviceBody['templateId'] = deviceTemplateId
        deviceBody = json.dumps(deviceBody)
        rq = requests.post(devicePostUrl, data=deviceBody, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        deviceResult = json.loads(rq.text)
        print(rq.text)
########Port Group handling##############
        portGroupPostUrl = "https://"+velo+".spirenteng.com/velocity/api/inventory/v8/device/" + deviceResult['id'] + "/port_group"
        groupBody = {}
        groupBody['name'] = 'Port Group ' + str(i)
        manualAssociations = {}
        manualAssociations['id'] = groupId
        groupBody['manualAssociations'] = [manualAssociations]
        groupBody = json.dumps(groupBody)
        rq = requests.post(portGroupPostUrl, data=groupBody, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        portGroupResult = json.loads(rq.text)
        #print(rq.text)
########Save group id as previous to link next time#####
        previousGroupId = portGroupResult['id']
########Ports handling#################################
        portPostUrl = "https://"+velo+".spirenteng.com/velocity/api/inventory/v8/device/" + deviceResult['id'] + "/ports"

        for d in portsBody['ports']:
            d.update({'groupId':portGroupResult['id']})
        portsBodyResult = json.dumps(portsBody.copy())
        rq = requests.post(portPostUrl, data=portsBodyResult, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
###################################
#######Reserve topologies##########
###################################
def reserveTopologies(velo, topologyIdList, start='', end='', duration='600'):
    postReservationUrl = "https://"+velo+".spirenteng.com/velocity/api/reservation/v11/reservation"
    for i,topId in enumerate(topologyIdList):
        time.sleep(5)
        raw = {}
        raw['name'] = 'Topology reservation test' + str(i)
        if duration:
            raw['duration'] = duration
        if start:
            raw['start'] = start
        if end:
            raw['end'] = end
        raw['topologyId'] = topId
        #print(raw)
        raw = json.dumps(raw)
        rq = requests.post(postReservationUrl, data=raw, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        print(rq.text)
###################################
#######Create Resources(PC)########
###################################        
def createResources(velo, qty='', startIndex='', stopIndex='', templateId=''):
    BaseUrl = "https://" + velo + ".spirenteng.com/velocity/api/inventory/v7/device"
    delUrl = "https://" + velo + "/velocity/api/inventory/v8/device/"
    templateId = 'fea52e8b-8d75-455e-baa5-80751d9625c7'
    toDelete = []
    if qty and startIndex: 
        stopIndex = qty + startIndex - 1 
    elif qty: 
        startIndex = 1
        stopIndex = qty
    for i in range(startIndex, stopIndex+1):
        raw = {}
        raw['name'] = 'RestApiPC' + str(i)
        raw['templateId'] = templateId
        body = json.dumps(raw.copy())
        rq = requests.post(BaseUrl, data=body, verify=False, auth=('spirent', 'spirent'),
                           headers={'Content-type': 'application/json'})
        result = json.loads(rq.text)
        if 'errorId' in rq.text:
            print('Resource creation error. Message: ' + result['message'])
        else:
            toDelete.append(result['id'])
        
    #cleanup(delUrl, toDelete)
    return delUrl, toDelete
################################################
#########Cleanup Procedure######################
################################################
def cleanup(toDelete={}):
    for keyUrl in toDelete:
        delList = toDelete[keyUrl]
        for elem in delList:
            delUrl = keyUrl + elem
            rq = requests.delete(delUrl, verify=False, auth=('spirent', 'spirent'))
            result = rq.text
            if 'error' in rq.text:
                print('Item delete error. Message: ' + result['message'])



############################
########Execute#############
############################
#reserveTopologies(vel, vSphereTopologyIdList, duration='120', start='1541069309000')
#createResources(vel, qty=1)
