#!/bin/bash

cat $1 $2 $3 | awk '{print $1, $2+$3+$4}' | sort -t ' '  -k 1,1 -u | sort -n -k2\
| awk '{print $1}' | head -1000  > task2.txt

echo "Finished, output is stored as task2.txt"
