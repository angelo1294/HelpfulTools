import restRequests
import yaml
import argparse
import atexit
import psutil

def ceva():
	print('something')

def updateToDelete(newDict, toUpdate):
	for key in newDict:
		for elem in newDict[key]:  
			try:
				toUpdate[key].append(elem)
			except:
				toUpdate[key] = newDict[key]
				break
	return toUpdate

def performanceUtilization():
	print('something')

def executionThread():
	########################
	###Variable Definition##
	########################
	velo = "vel-agrama-latest"
	toDelete = {}
	testResult = 0

	######At script exit -> call cleanup##############
	atexit.register(restRequests.cleanup, toDelete=toDelete, velo=velo, testResult=testResult)

	###################################################
	###Create resources and update cleaning object#####
	###################################################

	resources, testResult = restRequests.createResources(velo, 15)
	toDelete = updateToDelete(resources, toDelete)

	############################################
	###Publish topology and copy it X times#####
	############################################
	'''			X Topologies require X resources in order to reserve
	'''
	topologies, testResult = restRequests.createCopyTopologies(velo, 'topologies/Abstract_topology.yaml', qty=2, topologyName='PerformanceTestTopology')
	toDelete = updateToDelete(topologies, toDelete)

	#######################################################
	###Publish 5 layer subtopology and copy it X times#####
	#######################################################
	'''			X Topologies require 5X resources in order to reserve
	'''
	topologies, testResult = restRequests.createCopyTopologies(velo, 'topologies/5LayerTopology.yaml', qty=2, topologyName='Performance5LayerTestTopology')
	toDelete = updateToDelete(topologies, toDelete)

	############################################
	##########Reserve topologies################
	############################################
	reservations, testResult = restRequests.reserveTopologies(velo, topologies['topologyList'])
	toDelete = updateToDelete(reservations, toDelete)



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


if __name__ == '__main__':
	#executionThread()
	ceva()
