#! /usr/bin bash

FAST_DOWNWARD="/Users/Sayan/Desktop/Projects/downward/fast-downward.py"
PROBLEMS_DIR="$(pwd)/benchmarks/sasquatch/level*.sok"

rm -rf simulation
mkdir -p simulation

# Satisfying -> lama-first
# Optimizing -> seq-opt-bjolp
algorithms=(lama-first seq-opt-bjolp)

i=0
solved=0

for alg in $algorithms
do
    echo "Using $alg."
    for problem in $PROBLEMS_DIR
    do
        i=$((i+1))
        echo "Working on problem $i"

        python3 sokoban.py -f $FAST_DOWNWARD -i $problem -a $alg -t 1m > simulation/$alg-level-$i.out

        if [ $? -eq 124 ]
        then
            echo "Timed out."
        else
            echo "Done."
            solved=$((solved+1))
        fi
    done

    echo "Solved $solved/50 using $alg."

done
