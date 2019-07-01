#!/usr/bin/python3

import sys
import os

from encoding import minimal_encoding
from sys import stderr
from sudoku_io import parse_sudoku, parse_solver_output, clauses_to_cnf

if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print("Usage: python3 my_solver.py [sat_solver] [path_to_task]")
    #    sys.exit(1)

    #executable = sys.argv[0]
    #sat_solver = sys.argv[1]
    #path_to_task = sys.argv[2]
    #
    #print("running {} {} {}".format(executable, sat_solver, path_to_task), file=stderr)
    #
    #if os.path.basename(path_to_task) == "bsp-sudoku1.txt":
    #    sol_dir = os.path.dirname(path_to_task)
    #    sol_file = os.path.basename(path_to_task).replace(".txt", ".sol")
    #    with open("{}/{}".format(sol_dir, sol_file), "r") as f:
    #        for line in f:
    #            print(line)
    #print("done!", file=stderr)

    variables, constraints = parse_sudoku("/home/user/satSolving/sudoku-sat/examples/bsp-sudoku-input.txt")
    sat_problem = minimal_encoding(variables, constraints)
    print(clauses_to_cnf(sat_problem, variables))
