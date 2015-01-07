class Matrix(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._data = None

    @staticmethod
    def create_from_bitmap(width, height, bitmap, start_x, start_y):
        m = Matrix(width, height)

        m._data = list()
        for y in xrange(start_y, start_y + height):
            m._data.append(bitmap[y][start_x : start_x + width])
        m._data = tuple(m._data)

        return m

    @staticmethod
    def create_sub_matrix(matrix):
        m = Matrix(matrix._width, matrix._height - 1)
        m._data = matrix._data[1:]
        return m

    def __eq__(self, other):
        #if self._width != other._width or self._height != other._height:
        #    return False
        return self._data == other._data

    def __hash__(self):
        return hash((self._width, self._height, self._data))

    def __str__(self):
        output = list()
        for row in self._data:
            row_output = list()
            for col in row:
                if col:
                    row_output.append('1')
                else:
                    row_output.append('0')
            output.append(''.join(row_output))
        return '\n'.join(output)

    def is_qualified(self):
        if not any(self._data[0]):
            return False

        total = 0
        for row in self._data[1:]:
            #if not any(row):
            #    return False
            total += row.count(True)

        if total >= 4:
            return True
        else:
            return False

    def findall(self, bitmap):
        sub_matrix = Matrix.create_sub_matrix(self)

        matches = list()
        for w in xrange(80 - self._width):
            m = Matrix.create_from_bitmap(self._width, self._height - 1, bitmap, w, 0)
            if m == sub_matrix:
                for offset,bit_on in enumerate(self._data[0]):
                    if bit_on:
                        matches.append(w + 1 + offset)

        return matches
