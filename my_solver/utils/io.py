import re
import sys

from subprocess import Popen, PIPE
from utils.sudoku import Sudoku
from sys import stderr
import math

def parse_sudoku(sudoku_file):
    """
    Keyword arguments:
    sudoku_file -- string

    Returns:
    (Sudoku, string)
    """
    with open(sudoku_file, "r") as f:
        # Skip puzzle title, number of tasks, task number
        header = f.readline()
        header += f.readline()
        header += f.readline()
        last_header_line = f.readline()
        header += last_header_line[:-1]

        width = int(re.findall(r"\d+", last_header_line)[0])
        sudoku = Sudoku(width)
        constraints = set()

        row_index = 0
        for row in f:
            # Skip bars
            if row[0] == "+":
                continue

            row_entries = "".join(row.split("|")).split()
            for (column_index, entry) in enumerate(row_entries):
                if entry[0] == "_":
                    continue
                else:
                    sudoku.set_value_xy(row_index, column_index, int(entry))

            row_index += 1

    return (sudoku, header)

def clauses_to_cnf_file(clauses, sudoku, cnf_file):
    """
    Keyword arguments:
    clauses -- list(list(int))
    sudoku -- Sudoku
    cnf_file -- string
    """
    with open(cnf_file, "w") as f:
        print("p cnf {} {}".format(sudoku.get_max_index(), len(clauses)), file=f)

        for clause in clauses:
            print("{} 0".format(" ".join(map(lambda lit: str(lit), list(clause)))), file=f)

def call_solver(solver, cnf_file):
    """
    Keyword arguments:
    solver -- string
    cnf_file -- string

    Returns:
    string
    """
    if solver == "clasp":
        arguments = ["clasp", cnf_file]
    elif solver == "glucose":
        arguments = ["glucose", "-model", cnf_file]
    elif solver == "glucose-syrup":
        arguments = ["glucose-syrup", "-model", cnf_file]
    else:
        print("Unsupported solver!")
        sys.exit(1)

    p = Popen(arguments, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1)
    output, error = p.communicate()
    return output.decode("utf-8")

def parse_solver_output(output_str, sudoku):
    """
    SAT solvers show the satisfiability on a line prefixed with `s` and the
    model on one or many lines prefixed with `v`. This function parses this
    output and updates the given sudoku accordingly.

    Keyword arguments:
    output_str -- string
    sudoku -- Sudoku
    """
    for line in output_str.split("\n"):
        if not line or line[0] != "v":
            continue

        # Remove leading 'v'
        variable_assignments = line[1:].split()

        for assignment_str in variable_assignments:
            assignment = int(assignment_str)
            # Careful: can be trailing '0'
            if assignment > 0:
                sudoku.set_value(assignment)

    if sudoku.get_value(0, 0) == None:
        print("SAT solver evaluated Sudoku encoding as undecidable!", file=stderr)
        sys.exit(1)
