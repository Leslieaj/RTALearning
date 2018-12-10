mkdir result
for i in $(seq 1 20)
do
python ../generator.py 14_4_4
touch 14_4_4.json
cp 14_4_4.json 14_4_4-$i.json
python ../../learn.py 14_4_4-$i.json
done
