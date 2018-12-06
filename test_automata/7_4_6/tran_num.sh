#!/bin/sh

for i in $(seq 1 20)
do
python ../../rta.py 7_4_6-$i.json
done
