#!/usr/bin/env python3
import sys
import subprocess

with open(sys.argv[1], 'r') as of:
	files = of.readlines()
	for file in files:
		source = ".." + file.strip()
		old_substring = "jane"
		new_substring = "jdoe"
		new_name = file.replace(old_substring, new_substring)
		destination = ".." + new_name.strip()
		print("Moving {} to {}".format(source, destination))
		subprocess.run(["mv", source, destination])
