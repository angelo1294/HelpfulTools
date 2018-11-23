import restRequests
import yaml
import argparse
import atexit


def updateToDelete(newDict, toUpdate):
	for key in newDict:
		for elem in newDict[key]:  
			try:
				toUpdate[key].append(elem)
			except KeyError:
				toUpdate[key] = newDict[key]
				break
	return toUpdate

######Arguments parser##############
parser = argparse.ArgumentParser(description=
								"""NOTE: The given ranges of various elements creation 
									should be compatible with one another. (Number of 
									resources should coincide with number of topologies)""")

######Argument List###################
parser.add_argument('-resources', help="Number of resources to create. Nr of resources must be: topologies + 5*subtopologies", type=int)
parser.add_argument('-topologies', help="Number of topologies to create", type=int)
parser.add_argument('-subtopologies', help="Number of 5 layer topologies to create", type=int)
args = parser.parse_args()

########################
###Variable Definition##
########################
velo = "vel-agrama-latest"
toDelete = {}


'''			Beginning of Execution
'''
######At script exit -> call cleanup##############
atexit.register(restRequests.cleanup, toDelete=toDelete, velo=velo)

###################################################
###Create resources and update cleaning object#####
###################################################
'''			Beginning of Execution
'''
resources = restRequests.createResources(velo, args.resources)
toDelete = updateToDelete(resources, toDelete)

############################################
###Publish topology and copy it X times#####
############################################
'''			X Topologies require X resources in order to reserve
'''
topologies = restRequests.createCopyTopologies(velo, 'topologies/Abstract_topology.yaml', qty=args.topologies	, topologyName='PerformanceTest')
toDelete = updateToDelete(topologies, toDelete)

#######################################################
###Publish 5 layer subtopology and copy it X times#####
#######################################################
'''			X Topologies require 5X resources in order to reserve
'''
topologies = restRequests.createCopyTopologies(velo, 'topologies/5LayerTopology.yaml', qty=args.subtopologies, topologyName='Performance5LayerTest')
toDelete = updateToDelete(topologies, toDelete)

############################################
##########Reserve topologies################
############################################
reservations = restRequests.reserveTopologies(velo, topologies['topologyList'])
toDelete = updateToDelete(reservations, toDelete)

