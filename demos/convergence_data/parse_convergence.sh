#! /bin/bash
cat $1/*withpriorchange+annotation.dat | grep -v '#'  | awk '{print $1, $3}' > tmp.dat
cat  -n tmp.dat
