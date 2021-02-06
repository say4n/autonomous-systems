
# Autonomous Systems - Lab 2 - Modeling in SAT

# Getting Started

The fastest way to proceed for this lab session is:
1. Install any SAT solver e.g. from some [recent competition](http://www.satcompetition.org/).
   Other simple alternatives could be the _Glucose_ or the _Minisat_ solvers.
1. Write a script that generates the propositional formula describing the Sudoku instance you are dealing with, in CNF.
1. Print your representation of the formula into a file that follows the
   [DIMACS CNF format](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html), the standard
   format accepted by most SAT solvers.
1. Invoke the SAT solver you installed on the above file.
1. Parse the output of the SAT solver (an assignment of truth values to propositions printed in some form or another,
   depending on the solver you use) and convert it back into a solution to the original Sudoku problem.

We detail some of these steps below.

# Installing a SAT solver

You can install any of the SAT solvers available from the SAT competitions 
<http://www.satcompetition.org/>.
An easier alternative might be to use [Minisat](http://minisat.se/), a 
minimalistic but very efficient SAT solver. Under Ubuntu, you can install it
with:

    sudo apt install minisat

# Getting started with the coding

In the interest of time, we provide you with some code skeleton so that
you can focus on the interesting part of the submission, implementing the
propositional theory generator.

Clone this repository:

    git clone https://github.com/aig-upf/miis-autonomous-systems-20-21.git
    cd miis-autonomous-systems-20-21/lab2
  
You will see some Python code to get you started. 
It basically will handle command-line arguments for you, parse Sudoku boards
into a more meaningful matrix-like representation, write files in the 
DIMACS CNF format, and parse the output of the SAT solver.
The code assumes you are using Minisat,
but should be easy to modify it if you choose another solver. 
Look at the [sudoku.py](sudoku.py) and [utils.py](utils.py) files in the `lab2` directory.
You're not required to use any of this code for your submission,
but it might help you focus on the interesting parts. 

# A walkthrough of the exercise

To be more explicity about what needs to be done for the _programming_ exercises of this submission
(mostly exercises (b) and (c)):  

* To start programming exercise (b), you need to have an idea of how to "model" (cast, transform)
any given Sudoku instance as a (CNF) SAT problem. You should have done this in exercise (a).
This SAT problem is defined exactly by a formula in CNF, so you need to know what are the propositions, 
and what are the clauses in the SAT problem. The key idea with this type of _reductions_ is the following:
the CNF formula that you create for a given Sudoku instance will be satisfiable if and only if the Sudoku
is solvable. Furthermore, you will be able to read the actual Sudoku solution from any satisfying assignment
of the formula.

* Then you will need to write some kind of script that parses the input Sudoku board into some internal representation.
There is some sample code in the Python files in this directory that already does that for you, but of course you're
free to write your own routines.

* Once you have that, you will need to implement your transformation into a CNF formula. Most SAT solvers, also Minisat,
expect as input a file in the DIMACS CNF format. This is a very simple format with one line per clause of your formula,
where integer numbers are used to encode the literals. You can see a full description e.g. 
[here](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html). 
I have also uploaded a sample CNF I obtain with my (private :-)) solution to the assignment: see file [sample_cnf.cnf](sample_cnf.cnf).
This is the CNF that corresponds to the Sudoku board
`.......1.4.........2...........5.4.7..8...3....1.9....3..4..2...5.1........8.6...`.
You can call minisat, or whatever SAT solver you prefer, on this file:

        $ minisat sample_cnf.cnf 
        WARNING: for repeatability, setting FPU to use double precision
        ============================[ Problem Statistics ]=============================
        |                                                                             |
        |  Number of variables:           729                                         |
        |  Number of clauses:           11988                                         |
        |  Parse time:                   0.00 s                                       |
        |  Simplification time:          0.00 s                                       |
        |                                                                             |
        ============================[ Search Statistics ]==============================
        | Conflicts |          ORIGINAL         |          LEARNT          | Progress |
        |           |    Vars  Clauses Literals |    Limit  Clauses Lit/Cl |          |
        ===============================================================================
        ===============================================================================
        restarts              : 1
        conflicts             : 0              (0 /sec)
        decisions             : 1              (0.00 % random) (168 /sec)
        propagations          : 729            (122254 /sec)
        conflict literals     : 0              (-nan % deleted)
        Memory used           : 23.00 MB
        CPU time              : 0.005963 s
        
        SATISFIABLE

* The whole idea of exercise (b) is that you create this CNF file from any arbitrary Sudoku board, then
call a SAT solver (e.g. as a Python subprocess), read the satisfying assignment found by the solver, and
"translate" it back to the realm of Sudoku, so that you have a solved board.


