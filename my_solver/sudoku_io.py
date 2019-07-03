import re
import sys

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
                    constraints.add(variables.get_index(row_index, column_index, int(entry) - 1))

            row_index += 1

    return (variables, constraints)

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
        if line[0] == "v":
            variable_assignments = line[1:].split()
            print(variable_assignments)
            for assignment_str in variable_assignments:
                assignment = int(assignment_str)
                variables.set_value(abs(assignment), True if assignment > 0 else False)

    if variables.get_value(0, 0, 1) == None:
        print("Not every variable was assigned a truth value!", file=stderr)
        sys.exit(1)

def clauses_to_cnf(clauses, variables):
    """
    Keyword arguments:
    clauses -- list(list(int))
    variables -- Variables

    Returns:
    string
    """
    cnf = "p cnf {} {}".format(variables.get_max_index(), len(clauses))

    for clause in clauses:
        cnf += "\n"
        for literal in clause:
            cnf += str(literal) + " "
        cnf += "0"

    return cnf

def variables_to_sudoku(variables):
    """
    Keyword arguments:
    variables -- Variables

    Returns:
    string
    """
    width = variables.width
    char_length = int(math.log10(width))
    block_length = int(math.sqr(width))

    # build ending and starting line of sudoku frame
    block_line = "-" * ((char_length + 1) * block_length + 1)
    start_end_line = "+" + "+".join(block_line) + "+"
    print(start_end_line)

    for row_block in range(block_length):
        for  row in range(block_length):
            line = ""
            for col_block in range(block_length):
                block_line = "| "
                for col in range(block_length):
                    for number in range(width):
                        x = row_block * block_length + row + 1
                        y = col_block * block_length + col + 1
                        z = number + 1
                        if variables.get_value(x, y, z):
                            n = " " * (char_length - len(str(z))) + z + " "
                            block_line += n
                            break
                line += block_line
            line += "|"
            print(line)
        print(start_end_line)
