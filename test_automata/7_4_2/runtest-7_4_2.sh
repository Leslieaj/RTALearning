#!/bin/sh

mkdir result
for i in $(seq 1 20)
do
python ../generator.py
touch 7_4_2.json
cp 7_4_2.json 7_4_2-$i.json
python ../../learn.py 7_4_2-$i.json
done
