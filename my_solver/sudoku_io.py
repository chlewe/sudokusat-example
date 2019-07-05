import re
import sys

from subprocess import Popen, PIPE
from sudoku import Variables
from sys import stderr
import math

def parse_sudoku(sudoku_file):
    """
    Keyword arguments:
    sudoku_file -- string

    Returns:
    (Variables, set(int))
    """
    with open(sudoku_file, "r") as f:
        # Skip puzzle title, number of tasks, task number
        f.readline()
        f.readline()
        f.readline()

        width = int(re.findall(r"\d+", f.readline())[0])
        variables = Variables(width)
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
                    constraints.add(variables.get_index(row_index, column_index, int(entry)))

            row_index += 1

    return (variables, constraints)

def clauses_to_cnf_file(clauses, variables, cnf_file):
    """
    Keyword arguments:
    clauses -- list(list(int))
    variables -- Variables
    cnf_file -- string
    """
    with open(cnf_file, "w") as f:
        print("p cnf {} {}".format(variables.get_max_index(), len(clauses)), file=f)

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

def parse_solver_output(output_str, variables):
    """
    SAT solvers show the satisfiability on a line prefixed with `s` and the
    model on one or many lines prefixed with `v`. This function parses this
    output and updates the given variables accordingly.

    Keyword arguments:
    output_str -- string
    variables -- Variables
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
                variables.set_value(assignment)

    if variables.get_value(0, 0) == None:
        print("SAT solver evaluated Sudoku encoding as undecidable!", file=stderr)
        sys.exit(1)

def variables_to_sudoku(variables):
    """
    Keyword arguments:
    variables -- Variables

    Returns:
    string
    """
    width = variables.width
    subgrid_width = variables.subgrid_width
    cell_width = variables.cell_width
    subgrids_per_dim = variables.subgrids_per_dim

    # build ending and starting line of sudoku frame
    subgrid_bar = "-" * ((cell_width + 1) * subgrid_width + 1) + "+"
    horizontal_bar = "+" + subgrid_bar * subgrids_per_dim
    print(horizontal_bar)

    for subgrid_row in range(subgrids_per_dim):
        for row in range(subgrid_width):
            line = ""
            for subgrid_col in range(subgrids_per_dim):
                subgrid_line = "| "
                for col in range(subgrid_width):
                    x = subgrid_row * subgrid_width + row
                    y = subgrid_col * subgrid_width + col
                    number = str(variables.get_value(x, y))
                    subgrid_line += " " * (cell_width - len(number)) + number + " "
                line += subgrid_line
            line += "|"
            print(line)
        print(horizontal_bar)
