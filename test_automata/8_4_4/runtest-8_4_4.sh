mkdir result
for i in $(seq 1 20)
do
python ../generator.py 8_4_4
touch 8_4_4.json
cp 8_4_4.json 8_4_4-$i.json
python ../../learn.py 8_4_4-$i.json
done
