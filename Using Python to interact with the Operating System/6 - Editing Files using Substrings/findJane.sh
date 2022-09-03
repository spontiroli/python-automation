
#!/bin/bash

files=$(grep " jane " ../data/list.txt | cut -d ' ' -f 3)

for f in $files
do
	if test -e "..$f";
	then echo $f >> oldFiles.txt; 
	fi
done
