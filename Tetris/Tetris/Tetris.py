import os
import random
import time
import copy
import threading
import msvcrt

points = 0
figure_lock = threading.Lock()
draw_lock = threading.Lock()
game_over = False

class Field:
    def __init__(self):
        self.figure_list = []
        self.size_x = 12
        self.size_y = 20
        self.clean_field =[
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['+','-','-','-','-','-','-','-','-','-','-','+',],
    ]
        self.curr_field = []

    def fill(self, next_figure):
        if len(self.figure_list) == 0:
            self.curr_field = copy.deepcopy(self.clean_field)
            return

        new_field = copy.deepcopy(self.clean_field)

        for figure in self.figure_list:
            for piece in figure.pieces:
                y,x = piece
                new_field[y][x] = '#'

        for piece in next_figure.pieces:
            y,x = piece
            new_field[y+8][x+9] = '#'

        self.curr_field = new_field


    def draw(self):
        draw_lock.acquire()
        global points
        field_drawing_string = ''
        for y in range(4,self.size_y):
            for x in range(self.size_x):
                field_drawing_string += self.curr_field[y][x]          
            if y == 5:
                field_drawing_string += f' Points: {points}'
            if y == 7:
                field_drawing_string += ' next:'
            elif y in [8,9,10,11]:
                field_drawing_string += self.curr_field[y][13] + self.curr_field[y][14] + self.curr_field[y][15]
            field_drawing_string += '\n'

        os.system('cls')
        print(field_drawing_string)
        draw_lock.release()

    def remove_complete_rows(self):
        row_fill_counter = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for figure in self.figure_list:
            for piece in figure.pieces:
                row_fill_counter[piece[0]-4] +=1
        
        row_index = 4
        for row in row_fill_counter:
            if row == 10:
                 global points
                 points+= 20
                 for figure in self.figure_list:
                     piece_index = 0
                     for piece in copy.deepcopy(figure.pieces):
                         if piece[0] < row_index:
                             figure.pieces[piece_index][0] += 1
                         if piece[0] == row_index:
                             figure.pieces.remove(piece)
                         else:
                            piece_index += 1
            row_index +=1

    def game_over(self):
        self.curr_field[8][1]  = 'G'
        self.curr_field[8][2]  = 'A'
        self.curr_field[8][3]  = 'M'
        self.curr_field[8][4]  = 'E'
        self.curr_field[8][5]  = ' '
        self.curr_field[8][6]  = ' '
        self.curr_field[8][7]  = 'O'
        self.curr_field[8][8]  = 'V'
        self.curr_field[8][9]  = 'E'
        self.curr_field[8][10] = 'R'
                          

class Figure:
    def __init__(self):
        self.pieces = []
        self.rotate_state = True

    def check_moving_down_possible(self, curr_field):
        global game_over
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
                if piece[0] < 5:
                    game_over = True
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
        center = self.pieces[1]
        temp_piece = []
        for piece in self.pieces:
            distance = [center[0] - piece[0], center[1] - piece[1]]
            new_y = center[0] - distance[1]
            new_x = center[1] + distance[0]
            temp_piece.append([new_y, new_x])

        for temp_point in temp_piece:
            if temp_point in self.pieces:
                continue
            y, x = temp_point
            if field[y][x] in ['#', '|', '-']:
                return False
        return True


    def rotate(self):
        center = self.pieces[1]
        for piece in self.pieces:
            distance = [center[0] - piece[0],center[1] - piece[1]]
            piece[0] = center[0] - distance[1]
            piece[1] = center[1] + distance[0]

            



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
        self.rotate_state = True
        self.pieces = [[1,5],
                       [2,5],
                       [3,5],[3,6]]


class BigJ(Figure):
    def __init__(self):
        self.rotate_state = True
        self.pieces =       [[1,6],
                             [2,6],
                       [3,5],[3,6]]


class LongSquare(Figure):
    def __init__(self):
        self.rotate_state = True
        self.pieces = [[0,5],
                       [1,5],
                       [2,5],
                       [3,5],]


class ZigZagL(Figure):
    def __init__(self):
        self.rotate_state = True
        self.pieces = [[1,5],
                       [2,5],[2,6],
                             [3,6]]


class ZigZagR(Figure):
    def __init__(self):
        self.rotate_state = True
        self.pieces = [      [1,6],
                       [2,5],[2,6],
                       [3,5]]


class Bridge(Figure):
    def __init__(self):
        self.rotate_state = True
        self.pieces = [      [1,6],
                       [2,5],[2,6],
                             [3,6]]


field = Field()
curr_figure = Figure()
next_figure = BigL()

def player_input_thread():
    global game_over
    while not game_over:
        player_input = msvcrt.getch()
        update_necessary = False
        figure_lock.acquire()
        if player_input[0] == 97:
            if curr_figure.check_moving_left_possible(field.curr_field):
                curr_figure.move_left()
                update_necessary = True
        elif player_input[0] == 100:
            if curr_figure.check_moving_right_possible(field.curr_field):
                curr_figure.move_right()
                update_necessary = True
        elif player_input[0] == 115:
            if curr_figure.check_moving_down_possible(field.curr_field):
                curr_figure.move_down()
                update_necessary = True
        elif player_input[0] == 119:
            if curr_figure.check_rotate_possible(field.curr_field):
                curr_figure.rotate()
                update_necessary = True
        figure_lock.release()
        
        if update_necessary == True:
            figure_lock.acquire()
            field.fill(next_figure)
            figure_lock.release()
            field.draw()

player_thread = threading.Thread(target=player_input_thread)
player_thread.start()

needs_new_figure = True
speed = 0.5

while not game_over:
    figure_lock.acquire()
    field.fill(next_figure)
    figure_lock.release()
    field.draw()
    time.sleep(speed)

    if needs_new_figure:
        curr_figure = next_figure
        field.figure_list.append(curr_figure)
        figure_number = random.randint(0,6)
        if figure_number == 0:
            next_figure = Square()
        elif figure_number == 1:
            next_figure = BigL()
        elif figure_number == 2:
            next_figure = BigJ()
        elif figure_number == 3:
            next_figure = LongSquare()
        elif figure_number == 4:
            next_figure = ZigZagL()
        elif figure_number == 5:
            next_figure = ZigZagR()
        elif figure_number == 6:
            next_figure = Bridge()
        needs_new_figure = False
        if len(field.figure_list) != 0 and len(field.figure_list) % 5 == 0:
            if speed - 0.05 > 0:  
                speed -= 0.05

    figure_lock.acquire()
    if curr_figure.check_moving_down_possible(field.curr_field):
        curr_figure.move_down()
    else:
        needs_new_figure = True
        field.remove_complete_rows()
    figure_lock.release()

field.game_over()
field.draw()