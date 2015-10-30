#!/bin/bash

path="/home/jbroni/projects/a2tamil/data/01/*"

# setup index file
index_file="/home/jbroni/train_index_file.txt"
# clear index file
echo "" >> $index_file


for f in $path; do
	if [[ -d $f ]]; then
		for im in "$f/*.tiff"
		do
				echo "Processing $im"
        for im1 in $im
				do
					base=$(basename "$im1")
					#echo "Base $base"
					#echo "Basename : "
					base_name=${base%.*}
					#echo "calling python _main.py $im1 $base_name $f"
					python _main.py $im1 $base_name $f
					echo "$f/$base_name.jpg ${base_name:0:3}" >> $index_file
					#read -n1 -r -p "Press space to continue..." key
				done
		done
  fi
done
