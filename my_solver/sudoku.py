from math import floor, sqrt, log10

class Variables:
    def __init__(self, width):
        self.width = width
        self.subgrid_width = floor(sqrt(width))
        self.subgrids_per_dim = self.subgrid_width
        self.cell_width = floor(log10(width)) + 1

        self._values = [[None for y in range(width)] for x in range(width)]

    def get_index(self, row_x, column_y, number_z):
        return row_x * self.width ** 2 + column_y * self.width + number_z

    def get_value(self, row, column):
        return self._values[row][column]

    def set_value(self, index):
        row, column, number = self._index_to_coordinates(index)
        self._values[row][column] = number

    def get_max_index(self):
        return self.get_index(self.width - 1, self.width - 1, self.width)

    def _index_to_coordinates(self, index):
        number = index % self.width
        number = self.width if number == 0 else number
        column = (index - number) % (self.width ** 2) // self.width
        row = (index - column * self.width - number) // self.width ** 2
        return row, column, number

    def __str__(self):
        for x in range(self.width):
            line = ""
            for y in range(self.width):
                line += "{} ".format(self.get_value(x, y))

            print(line)
