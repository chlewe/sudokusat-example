#!/usr/bin/env python

import sys
import os

from utils.encoding import sudoku_to_clauses
from utils.io import *
from utils.signals import handler
from sys import stderr

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 my_solver.py [sat_solver] [path_to_task]")
        sys.exit(1)

    executable = sys.argv[0]
    sat_solver = sys.argv[1]
    path_to_task = sys.argv[2]

    print("running {} {} {}".format(executable, sat_solver, path_to_task), file=stderr)

    print("Generating CNF file...", file=stderr)
    sudoku, header = parse_sudoku(path_to_task)
    sat_problem = sudoku_to_clauses(sudoku)

    cnf_dir = os.path.dirname(__file__)
    cnf_basename = os.path.basename(path_to_task).replace(".txt", ".cnf")
    cnf_file = os.path.join(cnf_dir, "cnf-files", cnf_basename)
    if not os.path.exists(os.path.dirname(cnf_file)):
        os.makedirs(os.path.dirname(cnf_file))

    print("Saving clauses to \'{}\'...".format(cnf_file), file=stderr)
    clauses_to_cnf_file(sat_problem, sudoku, cnf_file)

    print("Waiting for SAT solver...", file=stderr)
    output = call_solver(sat_solver, cnf_file)

    print("Generating solution from solver output...", file=stderr)
    parse_solver_output(output, sudoku)

    print(header)
    print(sudoku)
    print("Done.", file=stderr)
