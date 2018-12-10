#!/bin/sh

for i in $(seq 1 20)
do
python ../../rta.py 3_3_3-$i.json
done
