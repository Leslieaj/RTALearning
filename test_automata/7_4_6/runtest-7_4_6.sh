#!/bin/sh

mkdir result
for i in $(seq 1 20)
do
python ../generator.py
touch 7_4_6.json
cp 7_4_6.json 7_4_6-$i.json
python ../../learn.py 7_4_6-$i.json
done
