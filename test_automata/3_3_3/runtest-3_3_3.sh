mkdir result
for i in $(seq 1 20)
do
python ../generator.py 3_3_3
touch 3_3_3.json
cp 3_3_3.json 3_3_3-$i.json
python ../../learn.py 3_3_3-$i.json
done
