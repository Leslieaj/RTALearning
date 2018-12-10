mkdir result
for i in $(seq 1 20)
do
python ../generator.py 4_4_4
touch 4_4_4.json
cp 4_4_4.json 4_4_4-$i.json
python ../../learn.py 4_4_4-$i.json
done
