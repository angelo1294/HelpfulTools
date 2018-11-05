import sys, paramiko, time

######################################################
#######Message is shown only in case of failing#######
######################################################
#Variables
hostname = ""
password = ""
username = ""
port = '22'
path = 'velocityAgent/' 
agentPath = 'https://jenkins-itest.spirenteng.com/jenkins/view/qa_itest/job/itest_Installer_rel_7x/lastSuccessfulBuild/artifact/artifacts/velocity-agent-linux.gtk.x86_64.zip'
requirements =['pool=driver', 'pool=startupteardown', 'pool=triggered']
#Connect via ssh 
try:
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname, port, username, password, allow_agent=False, look_for_keys=False)
	try:#Go to file and check if agent exists => if yes -> remove it and get new version
		stdin, stdout, stderr = client.exec_command('ls ' + path)
		if 'velocity-agent' in stdout.read().decode('ascii'):
			stdin, stdout, stderr = client.exec_command('rm -rf ' + path + 'velocity-agent')
		stdin, stdout, stderr = client.exec_command('wget '+ agentPath)
		exit_status = stdout.channel.recv_exit_status()
		if exit_status == 0:
			print("Get Velocity Agent zip successfull")
		else:
			print("Error when downloading agent: ", exit_status)
	except:
		print("Command failed to remove or get: " + stdout.read())
	try:
		stdin, stdout, stderr = client.exec_command('unzip velocity-agent-linux.gtk.x86_64.zip -d velocityAgent/')
		exit_status = stdout.channel.recv_exit_status()
		if exit_status == 0:
			print("Unzip finished")
		else:
			print("Error when extracting agent", exit_status)
		stdin, stdout, stderr = client.exec_command('rm -rf ' + 'velocity-agent-linux.gtk.x86_64.zip')
		stdin, stdout, stderr = client.exec_command("printf " 
													+ 	'"%s"' % ''.join([result+'\n' for result in requirements]) 
													+ "  >> " 
													+ path 
													+ "velocity-agent/configuration/agent.userdefined.capabilities")
	except:
		print("Extraction failed: " + stdout.read())
finally:
	client.close()
