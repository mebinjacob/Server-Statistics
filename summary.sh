#!/bin/bash

rm summary.txt
declare -a parent_folder=('/data/dataset/' '/data/tmp/');

folders=''
folder_sizes=''

echo "Size of folder Folder Path Number of files" >> summary.txt
for folder in ${parent_folder[@]}; 
do 
	folders=$(find $folder -maxdepth 1)
	for folder in $folders;
	do 
        	folder_sizes=$(du -sh $folder)
        	echo -n ' '$folder_sizes' ' >> summary.txt
        	find $folder -type f | wc -l  >> summary.txt
	done
done

echo "Summary of usage in folders : " >> summary.txt
echo "/data/dataset" >> summary.txt
df -h | grep '/data/dataset' >> summary.txt
df -h | grep '/data/tmp' >> summary.txt

echo "Docker images" >> summary.txt
docker images >> summary.txt

echo "Docker instances" >> summary.txt
docker ps -a >> summary.txt


sudo sa  -D --user-summary | awk -F " " '/.*/ {printf "%s ", $1; printf "%s " ,$4 ; printf "%s" ,$5; print " "}' >> temp.txt
sed -i '1d' temp.txt
echo "Summary of cpu and io usage per user!!" >> summary.txt
cat temp.txt >> summary.txt
cat summary.txt | mailx -s "Summary Report of SM321-01(Group Server)" mebinjacob@ufl.edu;cat summary.txt | mailx -s "Summary Report of SM321-01(Group Server)" daisyw@cise.ufl.edu
