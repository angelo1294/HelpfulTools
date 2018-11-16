import restRequests
import yaml
import argparse

######Arguments parser##############
parser = argparse.ArgumentParser(description=
								"""IMPORTANT NOTE: Set the required variables at the begining of the 
								script(such as version and VM list) before execution...
								Program receives the server address along with credentials and 
								updates the build of your VM list.""")

######Argument List###################
parser.add_argument('-resources', help="Number of resources to create", type=str)
parser.add_argument('-topologies', help="Number of topologies to create", type=str)
parser.add_argument('-passw', help="Password for vSphere server", type=str)
args = parser.parse_args()

########################
###Variable Definition##
########################
velo = 'vel-agrama-latest'
toDelete = {}


'''			Beginning of Execution
'''

###################################################
###Create resources and update cleaning object#####
###################################################
# delUrl, resourceIdList = restRequests.createResources(velo, args.resources)
# toDelete[delUrl] = resourceIdList

############################################
###Publish topology and copy it X times#####
############################################
# delUrl, topologyIdList = restRequests.createCopyTopologies(velo, 'Abstract_topology.yaml', qty=args.topologies, withResources=True)
# toDelete[delUrl] = topologyIdList

#restRequests.cleanup(toDelete)
