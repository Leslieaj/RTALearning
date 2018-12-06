#!/bin/sh

for i in $(seq 1 20)
do
python ../../rta.py 7_4_5-$i.json
done
