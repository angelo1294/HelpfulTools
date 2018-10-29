import requests 
import json, ast


vel = "vel-agrama-latest"
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
###############################
##Create topologies###########
###############################
def createCopyTopologies (velo, topologyId, qty='', startIndex='', stopIndex=''):
    BaseUrlPOST = "https://"+velo+".spirenteng.com/velocity/api/topology/v8/topology?copyFrom="+topologyId
    if qty and startIndex: 
        stopIndex = qty + startIndex - 1 
    elif qty: 
        startIndex = 1
        stopIndex = qty
    for i in range(startIndex, stopIndex+1):
        raw = {}
        raw['name'] = 'Leveling performance ' + str(i)
        raw['isAbstract'] = 'true'
        raw = json.dumps(raw)
        rq = requests.post(BaseUrlPOST, data=raw, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        result = json.loads(rq.text)
        BaseUrlPUT = "https://"+velo+".spirenteng.com/velocity/api/topology/v8/topology/" + result['id']
        body = {}
        body['isDraft'] = 'false'
        body = json.dumps(body)
        rq = requests.put(BaseUrlPUT, data=body, verify=False, auth=('spirent', 'spirent'),
                          headers={'Content-type': 'application/json'})
        topology = json.loads(rq.text)
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
##Create port groups###########Start from a parent device with port group and create devices and port groups linked to this parent#
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


#createPortGroups(vel,groupId = 'f8d5d66f-418b-4b90-96ca-73574916704a', deviceTemplateId='fea52e8b-8d75-455e-baa5-80751d9625c7', portTemplateId="a5266606-f35b-482b-8c3f-a4317c1ccbb9", qty=70, portsPerGroup=256)
createCopyTopologies(vel,topologyId='39f275d1-7d0c-45a0-bb07-96614b2011fe', qty=50)
