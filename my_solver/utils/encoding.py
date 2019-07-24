import sys

from utils.sudoku import Sudoku
from sys import stderr


def sudoku_to_clauses(sudoku):
    updated = True
    while updated:
        print("Computing naked singles...", file=stderr)
        updated = naked_singles(sudoku)

    clauses = preassigned_cells_to_unit_clauses(sudoku)
    clauses += extended_encoding(sudoku)
    return clauses


def preassigned_cells_to_unit_clauses(sudoku):
    clauses = list()
    width = sudoku.width
    subgrid_width = sudoku.subgrid_width

    for x in range(width):
        for y in range(width):
            z = sudoku.get_value(x, y)
            if z:
                clauses.append((sudoku.get_index(x, y, z), ))
                i, j = sudoku.xy_to_subgrid_ij(x, y)

                for x2 in range(width):
                    if x2 != x:
                        clauses.append((-sudoku.get_index(x2, y, z), ))
                for y2 in range(width):
                    if y2 != y:
                        clauses.append((-sudoku.get_index(x, y2, z), ))
                for rel_x2 in range(subgrid_width):
                    for rel_y2 in range(subgrid_width):
                        x2 = sudoku.rel_x_to_x(i, rel_x2)
                        y2 = sudoku.rel_y_to_y(j, rel_y2)
                        if x2 != x and y2 != y:
                            clauses.append((-sudoku.get_index(x2, y2, z), ))
                for z2 in range(1, width + 1):
                    if z2 != z:
                        clauses.append((-sudoku.get_index(x, y, z2), ))

    return clauses


def naked_singles(sudoku):
    width = sudoku.width
    subgrid_width = sudoku.subgrid_width
    updated = False

    seen_numbers_row = [set() for _ in range(width)]
    seen_numbers_column = [set() for _ in range(width)]
    seen_numbers_subgrid = [[set() for _ in range(subgrid_width)] for _ in range(subgrid_width)]

    numbers = set([i for i in range(1, width + 1)])

    for x in range(width): # row
        for y in range(width): # column
            z = sudoku.get_value(x, y)
            i, j = sudoku.xy_to_subgrid_ij(x, y)

            if z:
                seen_numbers_row[x].add(z)
                seen_numbers_column[y].add(z)
                seen_numbers_subgrid[i][j].add(z)

    for x in range(width):
        for y in range(width):
            if sudoku.get_value(x, y):
                continue
            i, j = sudoku.xy_to_subgrid_ij(x, y)
            missing_numbers = numbers - seen_numbers_row[x] - seen_numbers_column[y] - seen_numbers_subgrid[i][j]

            if len(missing_numbers) == 1:
                z = missing_numbers.pop()
                sudoku.set_value_xy(x, y, z)
                updated = True

    return updated


#def hidden_singles(sudoku):
#    width = sudoku.width
#    subgrid_width = sudoku.subgrid_width
#    updated = False
#
#    pos = [i for i in range(width)]
#    possible_number_pos_row = [[set(pos) for _ in range(width)] for _ in range(width)]
#    possible_number_pos_column = [[set(pos) for _ in range(width)] for _ in range(width)]
#
#    for x in range(width): # row
#        for y in range(width): # column
#            z = sudoku.get_value(x, y)
#            i, j = sudoku.xy_to_subgrid_ij(x, y)
#
#            if z:
#                for z2 in range(1, width + 1):
#                    if z2 != z:
#                        try:
#                            possible_number_pos_row[z2 - 1][x].remove(y)
#                        except KeyError:
#                            pass
#                        try:
#                            possible_number_pos_column[z2 - 1][y].remove(x)
#                        except KeyError:
#                            pass
#                possible_number_pos_row[z - 1][x] = { z - 1 }
#                possible_number_pos_column[z - 1][y] = { z - 1 }
#
#    # Hidden singles
#    for z in range(1, width + 1):
#        for x in range(width):
#            if len(possible_number_pos_row[z - 1][x]) == 1:
#                y = possible_number_pos_row[z - 1][x].pop()
#                print(x, y, z)
#                sudoku.set_value_xy(x, y, z)
#                updated = True
#        for y in range(width):
#            if len(possible_number_pos_column[z - 1][y]) == 1:
#                x = possible_number_pos_column[z - 1][y].pop()
#                print(x, y, z)
#                sudoku.set_value_xy(x, y, z)
#                updated = True
#
#    return updated


def minimal_encoding(sudoku):
    clauses = list()
    width = sudoku.width
    subgrid_width = sudoku.subgrid_width
    subgrids_per_dim = sudoku.subgrids_per_dim

    """
    Each cell has at least one number
    """
    for x in range(width):
        for y in range(width):
            if not sudoku.get_value(x, y):

                clause = list()
                for z in range(1, width + 1):
                    clause.append(sudoku.get_index(x, y, z))
                clauses.append(tuple(clause))

    """
    Each number occurs at most once per row
    """
    for x in range(width):
        for z in range(1, width + 1):
            if not z in sudoku.get_values_row(x):

                for y in range(width - 1):
                    for i in range(y + 1, width):
                        clause = (-sudoku.get_index(x, y, z), -sudoku.get_index(x, i, z))
                        clauses.append(clause)

    """
    Each number occurs at most once per column
    """
    for y in range(width):
        for z in range(1, width + 1):
            if not z in sudoku.get_values_column(y):

                for x in range(width - 1):
                    for i in range(x + 1, width):
                        clause = (-sudoku.get_index(x, y, z), -sudoku.get_index(i, y, z))
                        clauses.append(clause)

    """
    Each number occurs at most once per subgrid
    """
    for i in range(subgrids_per_dim):
        for j in range(subgrids_per_dim):
            for z in range(1, width + 1):
                if not z in sudoku.get_values_subgrid(i, j):

                    for rel_x1 in range(0, subgrid_width):
                        for rel_y1 in range(0, subgrid_width):
                            x1 = sudoku.rel_x_to_x(i, rel_x1)
                            y1 = sudoku.rel_y_to_y(j, rel_y1)

                            for rel_y2 in range(rel_y1 + 1, subgrid_width):
                                y2 = sudoku.rel_y_to_y(j, rel_y2)
                                clause = (-sudoku.get_index(x1, y1, z), -sudoku.get_index(x1, y2, z))
                                clauses.append(clause)

                            for rel_x2 in range(rel_x1 + 1, subgrid_width):
                                for rel_y3 in range(0, subgrid_width):
                                    x2 = sudoku.rel_x_to_x(i, rel_x2)
                                    y3 = sudoku.rel_y_to_y(j, rel_y3)
                                    clause = (-sudoku.get_index(x1, y1, z), -sudoku.get_index(x2, y3, z))
                                    clauses.append(clause)

    return clauses


def extended_encoding(sudoku):
    clauses = minimal_encoding(sudoku)
    width = sudoku.width
    subgrid_width = sudoku.subgrid_width
    subgrids_per_dim = sudoku.subgrids_per_dim

    """
    Each cell has at most one number
    """
    for x in range(width):
        for y in range(width):
            if not sudoku.get_value(x, y):

                for z in range(1, width):
                    for i in range(z + 1, width + 1):
                        clause = (-sudoku.get_index(x, y, z), -sudoku.get_index(x, y, i))
                        clauses.append(clause)

    """
    Each number occurs at least once per row
    """
    for x in range(width):
        for z in range(1, width + 1):
            if not z in sudoku.get_values_row(x):

                clause = list()
                for y in range(width):
                    clause.append(sudoku.get_index(x, y, z))
                clauses.append(tuple(clause))

    """
    Each number occurs at least once per column
    """
    for y in range(width):
        for z in range(1, width + 1):
            if not z in sudoku.get_values_column(y):

                clause = list()
                for x in range(width):
                    clause.append(sudoku.get_index(x, y, z))
                clauses.append(tuple(clause))

    """
    Each number occurs at least once per subgrid
    """
    for i in range(subgrids_per_dim):
        for j in range(subgrids_per_dim):
            for z in range(1, width + 1):
                if not z in sudoku.get_values_subgrid(i, j):

                    clause = list()
                    for rel_x in range(0, subgrid_width):
                        for rel_y in range(0, subgrid_width):
                            x = sudoku.rel_x_to_x(i, rel_x)
                            y = sudoku.rel_y_to_y(j, rel_y)
                            clause.append(sudoku.get_index(x, y, z))

                    clauses.append(tuple(clause))

    return clauses


#def visualise_clause(clause, sudoku):
#    return list(map(lambda x: ("+" if x >= 0 else "-") + str(sudoku._index_to_coordinates(abs(x))), clause))
