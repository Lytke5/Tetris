class Figure:
    def __init__(self):
        self.pieces = []

    def check_moving_down_possible(self, curr_field):
        lowest_pieces = []

        for piece in self.pieces:
            nothing_lower = True
            for p in self.pieces:
                if piece != p and piece[1] == p[1]:
                    if piece[0] < p[0]:
                        nothing_lower = False
            if nothing_lower:
                lowest_pieces.append(piece)

        for piece in lowest_pieces:
            if curr_field[piece[0]+1][piece[1]] == '#':
                return False
            elif curr_field[piece[0]+1][piece[1]] == '-':
                return False
        return True

    def check_moving_left_possible(self, curr_field):
        most_left_pieces = []

        for piece in self.pieces:
            nothing_more_left = True
            for p in self.pieces:
                if piece != p and piece[0] == p[0]:
                    if piece[1] > p[1]:
                        nothing_more_left = False
            if nothing_more_left:
                most_left_pieces.append(piece)

        for piece in most_left_pieces:
            if curr_field[piece[0]][piece[1]-1] == '#':
                return False
            elif curr_field[piece[0]][piece[1]-1] == '|':
                return False
        return True

    def check_moving_right_possible(self, curr_field):
        most_right_pieces = []

        for piece in self.pieces:
            nothing_more_right = True
            for p in self.pieces:
                if piece != p and piece[0] == p[0]:
                    if piece[1] < p[1]:
                        nothing_more_right = False
            if nothing_more_right:
                most_right_pieces.append(piece)

        for piece in most_right_pieces:
            if curr_field[piece[0]][piece[1]+1] == '#':
                return False
            elif curr_field[piece[0]][piece[1]+1] == '|':
                return False
        return True

    def move_down(self):                
        for piece in self.pieces:
            piece[0] += 1

    def move_left(self):                
        for piece in self.pieces:
            piece[1] -= 1

    def move_right(self):                
        for piece in self.pieces:
            piece[1] += 1

    def check_rotate_possible(self, field):
        pass

    def rotate(self):
        pass


class Square(Figure):
    def __init__(self):
        self.pieces = [[2,5],[2,6],
                       [3,5],[3,6]]

    def check_rotate_possible(self, field):
        return False

    def rotate(self):
        pass


class BigL(Figure):
    def __init__(self):
        self.pieces = [[1,5],
                       [2,5],
                       [3,5],[3,6]]

    def check_rotate_possible(self, field):
        center = self.pieces[0]
        if field[center][center-1] == '#':
            return False
        if field[center][center-2] == '#':
            return False
        if field[center+1][center-2] == '#':
            return False
        if field[center][center+1] == '#':
            return False
        return True

    def rotate(self):
        center = self.pieces[0]
        self.pieces[1] = [center,center-1]
        self.pieces[2] = [center,center-2]
        self.pieces[3] = [center+1,center-2]
        self.pieces[4] = [center][center+1]


class BigJ(Figure):
    def __init__(self):
        self.pieces =       [[1,6],
                             [2,6],
                       [3,5],[3,6]]

    def check_rotate_possible(self, field):
        center = self.pieces[0]
        if field[center][center-1] == '#':
            return False
        if field[center][center-2] == '#':
            return False
        if field[center+1][center-2] == '#':
            return False
        if field[center][center+1] == '#':
            return False
        return True

    def rotate(self):
        center = self.pieces[0]
        self.pieces[1] = [center,center-1]
        self.pieces[2] = [center,center-2]
        self.pieces[3] = [center+1,center-2]
        self.pieces[4] = [center][center+1]


class Long_Square(Figure):
    def __init__(self):
        self.pieces = [[0,5],
                       [1,5],
                       [2,5],
                       [3,5],]

    def check_rotate_possible(self, field):
        pass

    def rotate(self):
        pass

class Long_Square(Figure):
    def __init__(self):
        self.pieces = [[0,5],
                       [1,5],
                       [2,5],
                       [3,5],]

    def check_rotate_possible(self, field):
        pass

    def rotate(self):
        pass

class Long_Square(Figure):
    def __init__(self):
        self.pieces = [[0,5],
                       [1,5],
                       [2,5],
                       [3,5],]

    def check_rotate_possible(self, field):
        pass

    def rotate(self):
        pass



