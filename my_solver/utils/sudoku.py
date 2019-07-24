from math import floor, sqrt, log10

class Sudoku:
    def __init__(self, width):
        self.width = width
        self.subgrid_width = floor(sqrt(width))
        self.subgrids_per_dim = self.subgrid_width
        self.cell_width = floor(log10(width)) + 1

        self._values = [[None for y in range(width)] for x in range(width)]

    def get_index(self, x, y, z):
        return x * self.width ** 2 + y * self.width + z

    def get_value(self, x, y):
        return self._values[x][y]

    def set_value(self, index):
        x, y, z = self._index_to_coordinates(index)
        self._values[x][y] = z

    def set_value_xy(self, x, y, z):
        self._values[x][y] = z

    def get_max_index(self):
        return self.get_index(self.width - 1, self.width - 1, self.width)

    def _index_to_coordinates(self, index):
        z = index % self.width
        z = self.width if z == 0 else z
        y = (index - z) % (self.width ** 2) // self.width
        x = (index - y * self.width - z) // self.width ** 2
        return x, y, z

    def xy_to_subgrid_ij(self, x, y):
        return x // self.subgrid_width, y // self.subgrid_width

    def rel_x_to_x(self, i, rel_x):
        return self.subgrid_width * i + rel_x

    def rel_y_to_y(self, j, rel_y):
        return self.subgrid_width * j + rel_y


    def get_values_row(self, x):
        values = set()
        for y in range(self.width):
            z = self._values[x][y]
            if z:
                values.add(z)
        return values

    def get_values_column(self, y):
        values = set()
        for x in range(self.width):
            z = self._values[x][y]
            if z:
                values.add(z)
        return values

    def get_values_subgrid(self, i, j):
        values = set()
        for rel_x in range(self.subgrid_width):
            for rel_y in range(self.subgrid_width):
                x = self.rel_x_to_x(i, rel_x)
                y = self.rel_y_to_y(j, rel_y)
                z = self._values[x][y]
                if z:
                    values.add(z)
        return values

    def __str__(self):
        s = ""

        # build ending and starting line of sudoku frame
        subgrid_bar = "-" * ((self.cell_width + 1) * self.subgrid_width + 1) + "+"
        horizontal_bar = "+" + subgrid_bar * self.subgrids_per_dim
        s += horizontal_bar

        for subgrid_row in range(self.subgrids_per_dim):
            s += "\n"
            for row in range(self.subgrid_width):
                line = ""
                for subgrid_col in range(self.subgrids_per_dim):
                    subgrid_line = "| "
                    for col in range(self.subgrid_width):
                        x = self.rel_x_to_x(subgrid_row, row)
                        y = self.rel_y_to_y(subgrid_col, col)
                        z = self.get_value(x, y)
                        cell = str(z) if z else "_" * self.cell_width
                        subgrid_line += " " * (self.cell_width - len(cell)) + cell + " "
                    line += subgrid_line
                line += "|"
                s += line + "\n"
            s += horizontal_bar

        return s
