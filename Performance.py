import restRequests

########################
###Variable Definition##
########################
velo = 'vel-agrama-latest'
toDelete = {}


'''Beginning of method calling'''

###################################################
###Create resources and update cleaning object#####
###################################################
# delUrl, resourceIdList = restRequests.createResources(velo, 1)
# toDelete[delUrl] = resourceIdList

############################################
###Publish topology and copy it X times#####
############################################
topologyBody = open('Abstract_topology.yaml', 'r').readlines()
delUrl, topologyIdList = restRequests(velo, topologyBody, qty=1)