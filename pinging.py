import os

rackList = ['smt-c100-02', 'smt-c50-03', 'smt-c50-02', 'smt-c50-01', 'smt-c50-AUTO-02', 'smt-c100-01', 'smt-c100-03', 'smt-2u-01', 
			'smt-c50-04', 'smt-c100-04', 'smt-u2-02', 'smt-polaris-02', 'smt-c100-s3-01', 'smt-n11u-ms', 'smt-n11u-012', 'smt-n11u-01', 
			'smt-n11u-03', 'smt-9u-02', 'smt-n11u-ms-02', 'smt-n11u-021', 'smt-n11u-02', 'smt-n11u-01', 'smt-11u-01','smt-11u-02',
			'smt-c1-10g-02', 'smt-c1-bb-02', 'smt-c1-1g-02', 'smt-c1-nic63-02', 'smt-c1-nic62-01', 'smt-c1-avc-1g', 'smt-c1-avc-10g', 'smt-c1-1g-01', 
			'smt-c1-10g-01', 'smt-c1-bb-01', 'smt-c1-cv-01', 'smt-c1-bb-04', 'smt-c1-10g-04', 'smt-c1-1g-12', 'smt-c1-cv-04', 'smt-c1-cv-03', 'smt-c1-10g-03',
			'smt-c1-bb-03', 'smt-c1-1g-03', 'smt-c1-cv-03']
onlineList =[]
offlineList = []
for rack in rackList:
	response = os.system("ping " + rack + '.calenglab.spirentcom.com')
	if response == 0:
		onlineList.append(rack)
	else:
		offlineList.append(rack)
print('Online List: ' + str(onlineList))
print('Offline List: ' + str(offlineList))
print('Number of Online Hosts: ' + str(len(onlineList)))
