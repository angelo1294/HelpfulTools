#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -vcenter|--vcenter)
    vcenter="$2"
    shift # past argument
    shift # past value
    ;;
    -vel|--vel)
    vel="$2"
    shift # past argument
    shift # past value
    ;;
    -ite|--ite)
    ite="$2"
    shift # past argument
    shift # past value
    ;;
    -version|--version)
    version="$2"
    shift # past argument
    shift # past value
    ;;
    -user|--user)
    user="$2"
    shift # past argument
    shift # past value
    ;;
    -password|--password)
    password="$2"
    shift # past argument
    shift # past value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

###Replace said char with - ###
for var in {vcenter vel ite}; do
	$(echo $var) = tr - \\- 

###Install libraries###
# libsList=("pyyaml" "requests" "argparse" "psutil")
# for lib in ${libsList[@]}; do
# 	pip install $lib
# done

###Install powershell###
# if (! pswh)
# then
# 	wget -q https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb
# 	sudo dpkg -i packages-microsoft-prod.deb
# 	sudo apt-get update | echo Y
# 	sudo apt-get install -y powershell
# fi
###Execute script in powershell###
pwsh changeBuild.sh -vcenter $vcenter -version $version -user $user -password $password -ite $ite -vel $vel
###Check agent service###
# if ( (service velocity-agent status)>0 )
# then
# 	echo "Agent is ok"
# else
# 	chmod +x agent_service.sh
# 	echo "yes" | ./agent_service.sh -v ${v}
# fi

