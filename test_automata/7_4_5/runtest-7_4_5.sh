#!/bin/sh

mkdir result
for i in $(seq 1 20)
do
python ../generator.py
touch 7_4_5.json
cp 7_4_5.json 7_4_5-$i.json
python ../../learn.py 7_4_5-$i.json
done
