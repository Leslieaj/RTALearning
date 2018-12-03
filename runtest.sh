#!/bin/sh
for i in $(seq 1 10)
do
python learnrta.py test_automata/3_3_3.json & python learnrta.py test_automata/4_3_3.json
done
