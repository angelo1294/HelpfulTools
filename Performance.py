import threading
import restRequests
import yaml
import argparse
import atexit
import psutil, os
import time

###############################################
###Get time and convert it to human readable###
###############################################
def printRuntime(seconds):
	seconds = int(seconds)
	if seconds < 60:
		return str(seconds) + 's'
	elif seconds < 3600:
		minutes = seconds // 60
		seconds = seconds - 60*minutes
		return str(minutes) + 'm : ' + str(seconds) + 's'
	else:
		hours = seconds // 3600
		minutes = (seconds - 3600*hours) // 60
		seconds = seconds - 3600*hours - 60*minutes
		return hours + 'h : ' + minutes + 'm : ' + seconds + 's'

def updateToDelete(newDict, toUpdate):
	for key in newDict:
		for elem in newDict[key]:  
			try:
				toUpdate[key].append(elem)
			except:
				toUpdate[key] = newDict[key]
				break
	return toUpdate

##################################################
###Sample and output performance utilization data####
##################################################
def performanceUtilization(stop_event, interval):
	utilization = {'cpu': {'min': 0, 'max': 0, 'values':[]}, 'memory': {'min': 0, 'max': 0, 'values':[]}}
	startTime = time.clock()
	while not stop_event.is_set():
		try:
			utilization['cpu']['values'].append(psutil.cpu_percent(interval=interval))
			# utilization['memory']['values'].append(psutil.Process(os.getpid()).memory_info().rss / float(2 ** 20))
			utilization['memory']['values'].append(round(psutil.virtual_memory().used / float(2 ** 20)))
		except:
			print('ERROR when getting cpu/memory info')
	try:
		utilization['cpu']['min'] = min(utilization['cpu']['values'])
		utilization['cpu']['max'] = max(utilization['cpu']['values'])
		utilization['memory']['min'] = min(utilization['memory']['values'])
		utilization['memory']['max'] = max(utilization['memory']['values'])
	except:
		print('ERROR when assigning cpu/memory utilization data into dictionary')
	try:
		'''Output of CPU utilization '''
		print('- CPU utilization(%) - ') 
		print('Minimum: ' + str(utilization['cpu']['min'])) 
		print('Maximum: ' + str(utilization['cpu']['max'])) 
		print('Average: ' + str(round(sum( utilization['cpu']['values']) / len(utilization['cpu']['values']), 2)))
	except:
		print('ERROR when returning to output CPU utilization results')
	try:
		'''Output of Memory utilization '''
		print('- Memory utilization(Mbs) - ')
		print('Minimum: ' + str(utilization['memory']['min'])) 
		print('Maximum: ' + str(utilization['memory']['max']))
		print('Average: ' + str(round(sum( utilization['memory']['values']) / len(utilization['memory']['values']), 2)))
	except:
		print('ERROR when returning to output Memory utilization results')
	try:
		print('Execution time: ' + printRuntime(round(time.clock() - startTime)))
	except:
		print('ERROR when returning execution time')
	print('- Execution finished -')

###################################################
###Main execution thread for performance testing###
###################################################
def executionThread():
	'''Variable Definition'''
	velo = "vel-agrama-latest"
	toDelete = {}
	testResult = 0

	'''At script exit -> call cleanup'''
	atexit.register(restRequests.cleanup, toDelete=toDelete, velo=velo, testResult=testResult)
	
	'''Create resources and update cleaning object'''
	resources, testResult = restRequests.createResources(velo, agrs.resources)
	toDelete = updateToDelete(resources, toDelete)

	############################################
	###Publish topology and copy it X times#####
	############################################
	'''			X Topologies require X resources in order to reserve
	'''
	topologies, testResult = restRequests.createCopyTopologies(velo, 'topologies/Abstract_topology.yaml', qty=args.topologies, topologyName='PerformanceTestTopology')
	toDelete = updateToDelete(topologies, toDelete)

	#######################################################
	###Publish 5 layer subtopology and copy it X times#####
	#######################################################
	'''			X Topologies require 5X resources in order to reserve
	'''
	topologies, testResult = restRequests.createCopyTopologies(velo, 'topologies/5LayerTopology.yaml', qty=args.subtopologies, topologyName='Performance5LayerTestTopology')
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
	try:
		interval = 10				#Interval to get cpu/memory utilization
		pill2kill = threading.Event()
		t = threading.Thread(target=performanceUtilization, args=(pill2kill, interval))
		t.start()
		executionThread()
	except Exception as e:
		print("ERROR at creating performanceUtilization thread or starting of execution")
	finally:
		pill2kill.set()
		t.join()
