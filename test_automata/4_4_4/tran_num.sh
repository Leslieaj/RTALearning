#!/bin/sh

for i in $(seq 1 20)
do
python ../../rta.py 4_4_4-$i.json
done
