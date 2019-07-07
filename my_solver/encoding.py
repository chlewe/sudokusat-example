import sys

from sudoku import Variables

def minimal_encoding(variables, constraints):
    clauses = set()
    width = variables.width
    subgrid_width = variables.subgrid_width
    subgrids_per_dim = variables.subgrids_per_dim

    """
    Each cell has at least one number
    """
    for x in range(width):
        for y in range(width):
            clause = list()
            for z in range(1, width + 1):
                clause.append(variables.get_index(x, y, z))

            clauses.add(tuple(clause))

    """
    Each number occurs at most once per row
    """
    for z in range(1, width + 1):
        for y in range(width):
            for x in range(width - 1):
                for i in range(x + 1, width):
                    clause = (-variables.get_index(x, y, z), -variables.get_index(i, y, z))
                    clauses.add(clause)

    """
    Each number occurs at most once per column
    """
    for z in range(1, width + 1):
        for x in range(width):
            for y in range(width - 1):
                for i in range(y + 1, width):
                    clause = (-variables.get_index(x, y, z), -variables.get_index(x, i, z))
                    clauses.add(clause)

    """
    Each number occurs at most once per subgrid
    """
    for z in range(1, width + 1):
        for i in range(subgrids_per_dim):
            for j in range(subgrids_per_dim):
                for rel_x1 in range(0, subgrid_width):
                    for rel_y1 in range(0, subgrid_width):
                        x1 = subgrid_width * i + rel_x1
                        y1 = subgrid_width * j + rel_y1

                        for rel_y2 in range(rel_y1 + 1, subgrid_width):
                            y2 = subgrid_width * j + rel_y2
                            clause = (-variables.get_index(x1, y1, z), -variables.get_index(x1, y2, z))
                            clauses.add(clause)
                        for rel_x2 in range(rel_x1 + 1, subgrid_width):
                            for rel_y3 in range(0, subgrid_width):
                                x2 = subgrid_width * i + rel_x2
                                y3 = subgrid_width * j + rel_y3
                                clause = (-variables.get_index(x1, y1, z), -variables.get_index(x2, y3, z))
                                clauses.add(clause)

    """
    Each pre-assigned cell has the correct number
    """
    for name in constraints:
        clauses.add((name, ))

    #for clause in clauses:
    #    coord_clause = visualise_clause(clause, variables)
    #    print(coord_clause)

    return clauses


def extended_encoding(variables, constraints):
    clauses = minimal_encoding(variables, constraints)
    width = variables.width
    subgrid_width = variables.subgrid_width
    subgrids_per_dim = variables.subgrids_per_dim

    """
    Each cell has at most one number
    """
    for x in range(width):
        for y in range(width):
            for z in range(1, width):
                for i in range(z + 1, width + 1):
                    clause = (-variables.get_index(x, y, z), -variables.get_index(x, y, i))
                    clauses.add(clause)

    """
    Each number occurs at least once per row
    """
    for z in range(1, width + 1):
        for y in range(0, width):
            clause = list()
            for x in range(width):
                clause.append(variables.get_index(x, y, z))

            clauses.add(tuple(clause))

    """
    Each number occurs at least once per column
    """
    for z in range(1, width + 1):
        for x in range(width):
            clause = list()
            for y in range(width):
                clause.append(variables.get_index(x, y, z))

            clauses.add(tuple(clause))

    """
    Each number occurs at least once per subgrid
    """
    for i in range(subgrids_per_dim):
        for j in range(subgrids_per_dim):
            for rel_x in range(0, subgrid_width):
                for rel_y in range(0, subgrid_width):
                    x = subgrid_width * i + rel_x
                    y = subgrid_width * j + rel_y
                    clause = list()

                    for z in range(1, width + 1):
                        clause.append(variables.get_index(x, y, z))

                    clauses.add(tuple(clause))

    return clauses


def visualise_clause(clause, variables):
    return list(map(lambda x: ("+" if x >= 0 else "-") + str(variables._index_to_coordinates(abs(x))), clause))
