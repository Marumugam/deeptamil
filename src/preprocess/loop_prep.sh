#!/bin/bash

path="../../data/02/*.tiff"

for s in $path
do
	python _main.py ${s%.*}
done
