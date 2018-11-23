#!/bin/bash

libsList=("pyyaml" "requests")
for lib in ${libsList[@]}; do
	pip install $lib
done