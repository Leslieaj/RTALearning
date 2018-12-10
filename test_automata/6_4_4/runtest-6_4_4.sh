mkdir result
for i in $(seq 1 20)
do
python ../generator.py 6_4_4
touch 6_4_4.json
cp 6_4_4.json 6_4_4-$i.json
python ../../learn.py 6_4_4-$i.json
done
