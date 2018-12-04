#!/bin/bash

libsList=("pyyaml" "requests" "argparse" "psutil")
for lib in ${libsList[@]}; do
	pip install $lib
done