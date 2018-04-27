#!/usr/bin/env bash
MAX_THREADS=1

# Datasets
FILES=(
"datasets/ncol/astro-ph/astro-ph.ncol"
"datasets/gml/as-22july06/as-22july06.gml"
"datasets/ncol/condmat/condmat.ncol"
)

SIMILARITIES=("0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
cont=1
from=1
to=100
# Executes the python scripts for each file.
for f in $(seq 0 $((${#FILES[@]}-1)))
do
    # For each layer.
    for i in $(seq 0 $((${#SIMILARITIES[@]}-1)))
    do
        if [[ "$cont" -ge "$from" && "$cont" -le "$to" ]]
        then
            echo "Executing $cont to $((${#FILES[@]} * ${#SIMILARITIES[@]})): python main.py -f ${FILES[$f]} -s ${SIMILARITIES[$i]}"
            if [ "$MAX_THREADS" = 1 ]
            then
                python main.py -f ${FILES[$f]} -k 10 -s ${SIMILARITIES[$i]}
            else
                python main.py -f ${FILES[$f]} -k 10 -s ${SIMILARITIES[$i]} &
            fi
        fi
        cont=$(($cont + 1))
        while [ $( jobs | wc -l ) -ge "$MAX_THREADS" ]; do
        	sleep 0.5
        done
    done
done
