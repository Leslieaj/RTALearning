mkdir result
for i in $(seq 1 20)
do
python ../generator.py 10_4_4
touch 10_4_4.json
cp 10_4_4.json 10_4_4-$i.json
python ../../learn.py 10_4_4-$i.json
done
