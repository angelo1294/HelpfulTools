import requests 
import json, ast


vel = "vel-agrama-latest"
topologyIdList = ['84b239c7-a9b4-4d4d-8a70-8679c4d9e2ca', 'cbc768e9-5880-4175-81ab-abf0780f32cf', '5770acaf-196c-4603-8dc7-08b01c00febc', '5e9e298a-5c6c-49ab-ab1c-95b9a643edf2', '244f0679-012b-4804-8ff1-aa39c10ce1f9', '1d8a6279-9dc1-4b61-81e1-8e96854b7ca6', 'ba5db289-e925-4093-bec6-e82055f52005', '996041a6-7544-48ad-acb6-2ffbf812ee50', 'd7e11515-41c7-47c8-ab8d-198e0ed4a2da', 'bfd2ccea-fa5b-4ce0-9a7d-510790b0cbc0', 'ad233b8f-c5e3-4e65-9fa9-d3b7ebfc697a', 
'd1a5917b-4af3-44bb-8cde-f2677b4387ca', '4d6eb14a-1b4b-4d72-8c09-2aa08f246007', '49c4ebde-53c7-4e77-9eb9-b6dcbdf716a9']

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
##Create topologies############
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

############################
########Execute#############
############################
reserveTopologies(vel, topologyIdList, duration='120', start='1540820305000')
