#!/usr/bin/python3

import hashlib
import sys
import os

from encoding import *
from sudoku_io import *
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
    variables, constraints, header = parse_sudoku(path_to_task)
    sat_problem = extended_encoding(variables, constraints)

    header_hash = hashlib.md5()
    header_hash.update(header.encode('UTF-8'))
    cnf_dir = os.path.dirname(__file__)
    cnf_file = os.path.join(cnf_dir, "cnf-files", header_hash.hexdigest()) + ".cnf"
    clauses_to_cnf_file(sat_problem, variables, cnf_file)

    print("Waiting for SAT solver...", file=stderr)
    output = call_solver(sat_solver, cnf_file)

    print("Generating solution from solver output...", file=stderr)
    parse_solver_output(output, variables)

    variables_to_sudoku(variables, header)
    print("Done.", file=stderr)
