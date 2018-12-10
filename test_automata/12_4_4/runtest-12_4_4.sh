mkdir result
for i in $(seq 1 20)
do
python ../generator.py 12_4_4
touch 12_4_4.json
cp 12_4_4.json 12_4_4-$i.json
python ../../learn.py 12_4_4-$i.json
done
