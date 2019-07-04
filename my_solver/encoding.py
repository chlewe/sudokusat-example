import sys
from sudoku import Variables

def minimal_encoding(variables, constraints):
    clauses = list()
    width = variables.width
    grid_width = variables.grid_width
    grids_per_dim = variables.grids_per_dim

    """
    bigwedge_{x=1}^{9} bigwedge_{y=1}^{9} bigvee_{z=1}{9} s_xyz

    "Each cell has at least one number"
    """
    for x in range(width):
        for y in range(width):
            clause = list()
            for z in range(1, width + 1):
                clause.append(variables.get_index(x, y, z))

            clauses.append(clause)

    """
    bigwedge_{y=1}^{9} bigwedge_{z=1}^{9} bigwedge_{x=1}{8} bigwedge_{i=x+1}^{9} (neg s_xyz or neg x_iyz)

    "Each number occurs at most once per row"
    """
    # FIXME
    #for y in range(width):
    #    for z in range(1, width + 1):
    #        for x in range(width - 1):
    #            for i in range(x, width):
    #                clause = [-variables.get_index(x, y, z), -variables.get_index(i, y, z)]
    #                clauses.append(clause)

    """
    bigwedge_{x=1}^{9} bigwedge_{z=1}^{9} bigwedge_{y=1}{8} bigwedge_{i=y+1}^{9} (neg s_xyz or neg x_xiz)

    "Each number occurs at most once per column"
    """
    # FIXME
    #for x in range(width):
    #    for z in range(1, width + 1):
    #        for y in range(width - 1):
    #            for i in range(y, width):
    #                clause = [-variables.get_index(x, y, z), -variables.get_index(x, i, z)]
    #                clauses.append(clause)

    """
    bigwedge_{z=1}^{9} bigwedge_{i = 0}^{2} bigwedge_{j = 0}^{2} bigwedge_{x=1}^{3} bigwedge_{y=1}{3} bigwedge_{k=y+1}^{3} (neg s_(3i+x)(3j+y)z or neg x_(3i+x)(3j+k)z)
    """
    # FIXME
    #for z in range(width):
    #    for i in range(grids_per_dim):
    #        for j in range(grids_per_dim):
    #            for (x, y) in get_grid_xy(variables, i, j):
    #                for _x in range(x, i + grid_width):
    #                    clause = [-variables.get_index(x, y, z), -variables.get_index(_x, y, z)]
    #                    clauses.append(clause)

    #                for _y in range(y, j + grid_width):
    #                    clause = [-variables.get_index(x, y, z), -variables.get_index(x, _y, z)]
    #                    clauses.append(clause)

    """
    Already filled-in fields.
    """
    for name in constraints:
        clauses.append([name])

    return clauses


def get_grid_xy(variables, grid_row_x, grid_column_y):
    xy = list()
    for x in range(grid_row_x, grid_row_x + variables.grid_width):
        for y in range(grid_column_y, grid_column_y + variables.grid_width):
            xy.append((x, y))
    return xy
