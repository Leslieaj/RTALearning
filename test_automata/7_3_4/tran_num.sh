#!/bin/sh

for i in $(seq 1 20)
do
python ../../rta.py 7_3_4-$i.json
done
