#!/bin/bash

libsList=("pyyaml" "requests" "argparse" "psutil")
for lib in ${libsList[@]}; do
	pip install $lib
done
if ( (service velocity-agent status)>0 )
then
	echo "Agent is ok"
else
	chmod +x agent_service.sh
	echo "yes" | ./agent_service.sh
fi

