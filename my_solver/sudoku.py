from math import floor, sqrt

_next_index_counter = 0
def _next_index():
    global _next_index_counter
    _next_index_counter += 1
    return _next_index_counter

_xyz_index_bijection = set()

def _get_index(x, y, z):
    for (xyz, index) in _xyz_index_bijection:
        if (x, y, z) == xyz:
            return index

    index = _next_index()
    _xyz_index_bijection.add(((x, y, z), index))
    return index

def _get_xyz(index):
    for ((x, y, z), _index) in _xyz_index_bijection:
        if index == _index:
            return (x, y, z + 1)
    return None

def _index_to_coordinates(index):
    return _get_xyz(index)


class Variables:
    def __init__(self, width):
        self.width = width
        self.grid_width = floor(sqrt(width))
        self.grids_per_dim = self.width // self.grid_width
        self._indices = [[[_get_index(x, y, z) for z in range(width)] for y in range(width)] for x in range(width)]
        self._values = [[[None for z in range(width)] for y in range(width)] for x in range(width)]

    def get_index(self, row_x, column_y, number_z):
        return self._indices[row_x][column_y][number_z - 1]

    def get_value(self, row_x, column_y, number_z):
        return self._values[row_x][column_y][number_z - 1]

    def set_value(self, index, value):
        row_x, column_y, number_z = _index_to_coordinates(index)
        self._values[row_x][column_y][number_z - 1] = value

    def get_max_index(self):
        return _next_index_counter

    def __str__(self):
        variables_str = ""
        for x in range(self.width):
            for y in range(self.width):
                variables_str += "({:2},{:2}): {}\n".format(x, y, self._indices[x][y])
        for x in range(self.width):
            for y in range(self.width):
                variables_str += "({:2},{:2}): {}\n".format(x, y, self._values[x][y])

        return variables_str
