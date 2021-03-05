#! /usr/bin/env python3

import subprocess
import time

CONFIGS = {
    "sat": {
        "astar_goalcount" : ["--search", "astar(goalcount)"],
        "eager_greedy_ff" : ["--heuristic", "h=ff()", "--search", "eager_greedy([h], preferred=[h])"],
        "eager_greedy_add" : ["--heuristic", "h=add()", "--search", "eager_greedy([h], preferred=[h])"]
    },
    "opt": {
        "astar_blind" : ["--search", "astar(blind)"],
        "astar_lmcut" : ["--search", "astar(lmcut)"],
        "astar_hmax" : ["--search", "astar(hmax)"]
    }
}

FAST_DOWNWARD = "/Users/Sayan/Desktop/Projects/downward/fast-downward.py"

if __name__ == "__main__":
    subprocess.run("rm -rf simulation".split(" "))
    subprocess.run("mkdir -p simulation".split(" "))

    for nature in CONFIGS:
        for i, level in enumerate(["benchmarks/sasquatch/level1.sok", "benchmarks/sasquatch/level2.sok"]):
            subprocess.run(["python3", "sokoban.py", "-i", level])

            for algorithm in CONFIGS[nature]:
                with open(f"simulation/level-{i}-{algorithm}.out", "wt") as stdout:
                    print(f"Working on level {i} using {algorithm}.")

                    then = time.time()
                    subprocess.run([FAST_DOWNWARD, "sokoban-domain.pddl", "sokoban-instance.pddl"] + CONFIGS[nature][algorithm],
                                    stdout=stdout)
                    delta = time.time() - then

                    print(f"Solved level{i}.sok with {algorithm} in {delta}s.")
