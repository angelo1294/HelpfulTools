#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -v|--velocity)
    EXTENSION="$2"
    shift # past argument
    shift # past value
    ;;
esac
done


libsList=("pyyaml" "requests" "argparse" "psutil")
for lib in ${libsList[@]}; do
	pip install $lib
done
if ( (service velocity-agent status)>0 )
then
	echo "Agent is ok"
else
	chmod +x agent_service.sh
	echo "yes" | ./agent_service.sh -v ${VELOCITY}
fi

