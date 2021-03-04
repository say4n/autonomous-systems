#! /usr/bin bash

FAST_DOWNWARD="/Users/Sayan/Desktop/Projects/downward/fast-downward.py"

rm -rf simulation
mkdir -p simulation

problems=("$(pwd)/benchmarks/sasquatch/level1.sok" "$(pwd)/benchmarks/sasquatch/level2.sok")
algorithms=(seq-sat-lama-2011 seq-sat-fd-autotune-1 seq-sat-fdss-1 seq-opt-lmcut seq-opt-fd-autotune seq-opt-bjolp)

i=0
solved=0

for alg in $algorithms
do
    for problem in $problems
    do
        i=$((i+1))

        SECONDS=0
        python3 sokoban.py -f $FAST_DOWNWARD -i $problem -a $alg > simulation/$alg-level-$i.out
        duration=$SECONDS

        echo "Solved $problem with $alg in $(($duration / 60)) minutes and $(($duration % 60)) seconds."
    done

    echo "Solved $solved/50 using $alg."

done
