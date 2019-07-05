import sys

from sudoku import Variables

def minimal_encoding(variables, constraints):
    clauses = list()
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

            clauses.append(clause)

    """
    Each number occurs at most once per row
    """
    for z in range(1, width + 1):
        for y in range(width):
            for x in range(width - 1):
                for i in range(x + 1, width):
                    clause = [-variables.get_index(x, y, z), -variables.get_index(i, y, z)]
                    clauses.append(clause)

    """
    Each number occurs at most once per column
    """
    for z in range(1, width + 1):
        for x in range(width):
            for y in range(width - 1):
                for i in range(y + 1, width):
                    clause = [-variables.get_index(x, y, z), -variables.get_index(x, i, z)]
                    clauses.append(clause)

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
                            y2 = subgrid_width * i + rel_y2
                            clause = [-variables.get_index(x1, y1, z), -variables.get_index(x1, y2, z)]
                            clauses.append(clause)
                        for rel_x2 in range(rel_x1 + 1, subgrid_width):
                            x2 = subgrid_width * i + rel_x2
                            clause = [-variables.get_index(x1, y1, z), -variables.get_index(x2, y1, z)]
                            clauses.append(clause)

    """
    Already filled-in fields.
    """
    for name in constraints:
        clauses.append([name])

    #for clause in clauses:
    #    coord_clause = visualise_clause(clause, variables)
    #    print(coord_clause)

    return clauses


def visualise_clause(clause, variables):
    return list(map(lambda x: ("+" if x >= 0 else "-") + str(variables._index_to_coordinates(abs(x))), clause))
