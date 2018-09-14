from pexpect import pxssh
import ipaddress

def networksToHosts(listOfNetworks):
	listOfHosts = []
	for elem in listOfNetworks:
		network = ipaddress.ip_network(elem)
		for host in network.hosts():
			listOfHosts.append(str(host))
	return listOfHosts

listOfNetworks = ['10.109.14.0/24', '10.109.15.0/24', '10.109.31.0/24', '10.109.32.0/24']
#listOfHosts = networksToHosts(listOfNetworks)
listOfHosts = ['qa-u16-ipopescu2.spirenteng.com']
for host in listOfHosts:
	try:
		s = pxssh.pxssh(timeout=2)
		hostname = host
		username = 'root'
		password = 'aMP#JANH'
		s.login(hostname, username, password, login_timeout=2)
		s.sendline('hostname -s')
		s.prompt()
		print("Sucessfull login on: "+ hostname + " Hostname: " + str(s.before))
		s.logout()
	except pxssh.ExceptionPxssh:
		print("Fail login on: "+ hostname)
