#!/bin/sh

for i in $(seq 1 20)
do
python ../../rta.py 14_4_4-$i.json
done
