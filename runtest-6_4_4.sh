#!/bin/sh

mkdir test_automata/6_4_4
mkdir test_automata/6_4_4/result
for i in $(seq 1 20)
do
python test_automata/generator.py
touch test_automata/6_4_4/6_4_4-$i.json
cp test_automata/6_4_4.json test_automata/6_4_4/6_4_4-$i.json
python learn.py test_automata/6_4_4/6_4_4-$i.json
done
