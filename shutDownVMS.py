import paramiko

listOfVMS = ['ite-agrama-latest', 'ite-agrama-pan1', 'ite-agrama-ldap', 'ite-61-agrama', 'ite-70-agrama', 
			'qa-u16-agrama', 'vel-61-agrama', 'vel-71-agrama', 'vel-agrama-pan1', 'vel-agrama-latest']
#listOfVMS = ['ite-agrama-ldap']
endOfDNS = '.spirenteng.com'
passList = []
failList = []
for host in listOfVMS:
	try:
		print("Step for: "+ host)
		s = paramiko.SSHClient()
		s.load_system_host_keys()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		hostname = host + endOfDNS
		username = 'root'
		password = 'admin'
		s.connect(
            hostname,
            '22',
            username,
            password,
            timeout=1,
            allow_agent=False,
            look_for_keys=False
            )
		print("Sucessfull login")
		ssh_stdin, ssh_stdout, ssh_stderr = s.exec_command("shutdown now")
		print("shutdown successful\n")
		passList.append(host)
		s.close()
	except :
		print("Fail job\n")
		failList.append(host)
print("Passed: " + str(passList))
print("Failed: " + str(failList))

