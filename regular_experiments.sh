#!/usr/bin/env bash
MAX_THREADS=1

# Datasets
FILES=(
"datasets/gml/dolphins/dolphins.gml"
"datasets/pajek/yeast/YeastL.net"
"datasets/ncol/netscience/netscience.ncol"
"datasets/ncol/facebook/facebook.ncol"
"datasets/ncol/geom/geom.ncol"
"datasets/ncol/power/power.ncol"
"datasets/gml/hep-th/hep-th.gml"
)

SIMILARITIES=("6")
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
            echo "Executando $cont de $((${#FILES[@]} * ${#SIMILARITIES[@]})): python coarsening_main.py -f ${FILES[$f]} -s ${SIMILARITIES[$i]}"
            if [ "$MAX_THREADS" = 1 ]
            then
                python coarsening_main.py -f ${FILES[$f]} -k 10 -s ${SIMILARITIES[$i]}
            else
                python coarsening_main.py -f ${FILES[$f]} -k 10 -s ${SIMILARITIES[$i]} &
            fi
        fi
        cont=$(($cont + 1))
        while [ $( jobs | wc -l ) -ge "$MAX_THREADS" ]; do
        	sleep 0.5
        done
    done
done
