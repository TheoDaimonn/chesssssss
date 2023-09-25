x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
y_axis = ['1', '2', '3', '4', '5', '6', '7', '8']
figures_weights = {
    'pawn': 10,
    'bishop': 30,
    'knight': 30,
    'rook': 50,
    'queen': 90,
    'king': 900
}



class Board():
    def __init__(self, coords: dict()):
        self.figures_coords = coords
        self.kings_pos = {
            'white': 'd8',
            'black': 'd1'
        }
        self.figures_on_board = {
        'white': {
            'pawn': 8,
            'bishop': 2,
            'knight': 2,
            'rook': 2,
            'queen': 1,
            'king': 1
            },
        'black': {
            'pawn': 8,
            'bishop': 2,
            'knight': 2,
            'rook': 2,
            'queen': 1,
            'king': 1
            }
        }
    
    def show(self):
        for_show = [[None for _ in range(8)] for __ in range(8)]
        for y in range(8):
            for x in range(8):
                if self.figures_coords[y_axis[y]][x_axis[x]] is None: for_show[y][x] = '   '
                else: for_show[y][x] = self.figures_coords[y_axis[y]][x_axis[x]].get_symbol()
        Board_view_decorate(for_show)
        
    def get_figures_coords(self):
        return self.figures_coords

    def get_kings_position(self):
        return self.kings_pos

    def get_figure_type_on_place(self, place: str()):
        return self.figures_coords[place[-1]][place[0]].get_type()
    
    def get_figure_team_on_place(self, place: str()):
        return self.figures_coords[place[-1]][place[0]].get_team()

    def swap(self, cur_place: str(), new_place: str()):
        if self.figures_coords[new_place[-1]][new_place[0]] is not None and self.figures_coords[new_place[-1]][new_place[0]].get_type() == 'king':
            self.figures_coords[new_place[-1]][new_place[0]] = self.figures_coords[cur_place[-1]][cur_place[0]]
            self.figures_coords[cur_place[-1]][cur_place[0]] = None
            return True

        
        self.figures_coords[new_place[-1]][new_place[0]] = self.figures_coords[cur_place[-1]][cur_place[0]]
        self.figures_coords[cur_place[-1]][cur_place[0]] = None
        return False

    def scores(self, team: str()):
        s = 0
        for item in self.figures_on_board[team]:
            s += self.figures_on_board[team][item] * figures_weights[item]
        return s





class Figure():
    def __init__(self, figure_type: str(), team: str(), symbol: str()):
        self.type = figure_type
        self.team = team
        self.symbol = symbol

    def get_team(self):
        return self.team

    def get_type(self):
        return self.type

    def get_symbol(self):
        return self.symbol


def Team_init():
    figuresWhite = {
        'king': ' ♔ ',
        'queen': ' ♕ ',
        'rook': ' ♖ ',
        'bishop': ' ♗ ',
        'knight': ' ♘ ',
        'pawn': ' ♙ '
        }
    figuresBlack = {
        'king': ' ♚ ', 
        'queen': ' ♛ ',
        'rook': ' ♜ ',
        'bishop': ' ♝ ',
        'knight': ' ♞ ',
        'pawn': ' ♟ '
        }
    return {'white': figuresWhite, 'black': figuresBlack}


def First_realize():
    symboles = Team_init()
    coords = {f'{__ + 1}': {chr(97 + _): None for _ in range(8)} for __ in range(8)}
    helper = ['rook', 'knight', 'bishop','queen','king','bishop','knight', 'rook']
    for x in zip(x_axis, helper):
        coords['1'][x[0]] = Figure(x[-1], 'black', symboles['black'][x[-1]])
        coords['2'][x[0]] = Figure('pawn', 'black', symboles['black']['pawn'])
        coords['7'][x[0]] = Figure('pawn', 'white', symboles['white']['pawn'])
        coords['8'][x[0]] = Figure(x[-1], 'white', symboles['white'][x[-1]])

    return coords


def Board_view_decorate(current_view: list()):
    line_spacing = '   ' + '+---' * 8 + '+'
    for line in range(len(current_view)):
        print(line_spacing)
        print(' {} '.format(line + 1) + '|' + '|'.join(current_view[line]) + '|')
    print(line_spacing)
    print('     A   B   C   D   E   F   G   H  ')    


def Pawn_movement(place: dict(), team: str(), all_coords: dict()):
    (x, y, moves) = (place[0], int(place[-1]), [])
    if team == 'white':
        if y == 7:
            if all_coords[f'{y - 1}'][x] is None and all_coords[f'{y - 2}'][x] is None:
                moves.append(x + f'{y - 1}')
                moves.append(x + f'{y - 2}')
        elif y < 7 and y >= 2 and all_coords[f'{y - 1}'][x] is None:
            moves.append(x + f'{y - 1}')
        moves += Pawn_kill(place, team, all_coords)
    else:
        if y == 2:
            if all_coords[f'{y + 1}'][x] is None and all_coords[f'{y + 2}'][x] is None:
                moves.append(x + f'{y + 1}')
                moves.append(x + f'{y + 2}')
        elif y > 2 and y <= 7 and all_coords[f'{y + 1}'][x] is None:
            moves.append(x + f'{y + 1}')
        moves += Pawn_kill(place, team, all_coords)
    return moves


def Pawn_kill(place: dict(), team: str(), all_coords: dict()):
    (x, moves) = (x_axis.index(place[0]), [])
    if team == 'white':
        y = f'{int(place[-1]) - 1}'
        if x > 0 and x < 7:
            if all_coords[y][x_axis[x - 1]] is not None and all_coords[y][x_axis[x - 1]].get_team() != team:
                moves.append(x_axis[x - 1] + y)
            elif all_coords[y][x_axis[x + 1]] is not None and all_coords[y][x_axis[x + 1]].get_team() != team:
                moves.append(x_axis[x + 1] + y)
        elif x == 0 and all_coords[y][x_axis[x + 1]] is not None and all_coords[y][x_axis[x + 1]].get_team() != team:
            moves.append(x_axis[x + 1] + y)
        elif x == 7 and all_coords[y][x_axis[x - 1]] is not None and all_coords[y][x_axis[x - 1]].get_team() != team:
            moves.append(x_axis[x - 1] + y)
    else:
        y = f'{int(place[-1]) + 1}'
        if x > 0 and x < 7:
            if all_coords[y][x_axis[x - 1]] is not None and all_coords[y][x_axis[x - 1]].get_team() != team:
                moves.append(x_axis[x - 1] + y)
            elif all_coords[y][x_axis[x + 1]] is not None and all_coords[y][x_axis[x + 1]].get_team() != team:
                moves.append(x_axis[x + 1] + y)
        elif x == 0 and all_coords[y][x_axis[x + 1]] is not None and all_coords[y][x_axis[x + 1]].get_team() != team:
            moves.append(x_axis[x + 1] + y)
        elif x == 7 and all_coords[y][x_axis[x - 1]] is not None and all_coords[y][x_axis[x - 1]].get_team() != team:
            moves.append(x_axis[x - 1] + y)
    
    return moves


def Bishop_movement(place: dict(), team: str(), all_coords: dict()):
    (x, y, moves) = (x_axis.index(place[0]), int(place[-1]) - 1, [])
    (xd, yd) = (x, y)
    while xd < 7 and yd < 7:
        xd += 1
        yd += 1
        if all_coords[y_axis[yd]][x_axis[xd]] is None: moves.append(x_axis[xd] + y_axis[yd])
        elif all_coords[y_axis[yd]][x_axis[xd]] is not None and all_coords[y_axis[yd]][x_axis[xd]].get_team() != team:
            moves.append(x_axis[xd] + y_axis[yd])
            break
        else: break
    (xd, yd) = (x, y)
    while xd > 0 and yd < 7:
        xd -= 1
        yd += 1
        if all_coords[y_axis[yd]][x_axis[xd]] is None: moves.append(x_axis[xd] + y_axis[yd])
        elif all_coords[y_axis[yd]][x_axis[xd]] is not None and all_coords[y_axis[yd]][x_axis[xd]].get_team() != team:
            moves.append(x_axis[xd] + y_axis[yd])
            break
        else: break
    (xd, yd) = (x, y)
    while xd < 7 and yd > 0:
        xd += 1
        yd -= 1
        if all_coords[y_axis[yd]][x_axis[xd]] is None: moves.append(x_axis[xd] + y_axis[yd])
        elif all_coords[y_axis[yd]][x_axis[xd]] is not None and all_coords[y_axis[yd]][x_axis[xd]].get_team() != team:
            moves.append(x_axis[xd] + y_axis[yd])
            break
        else: break
    (xd, yd) = (x, y)
    while xd > 0 and yd > 0:
        xd -= 1
        yd -= 1
        if all_coords[y_axis[yd]][x_axis[xd]] is None: moves.append(x_axis[xd] + y_axis[yd])
        elif all_coords[y_axis[yd]][x_axis[xd]] is not None and all_coords[y_axis[yd]][x_axis[xd]].get_team() != team:
            moves.append(x_axis[xd] + y_axis[yd])
            break
        else: break
    return moves


def Knight_movement(place: dict(), team: str(), all_coords: dict()):
    (x, y, moves) = (x_axis.index(place[0]) + 1, int(place[-1]), [])
    moves_checker = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
    for axis in moves_checker:
        (xd, yd) = (x + axis[0], y + axis[-1])
        if 0 < xd < 9 and 0 < yd < 9 and all_coords[y_axis[yd - 1]][x_axis[xd - 1]] is None:
            moves.append(f'{x_axis[xd - 1]}{yd}')
        elif 0 < xd < 9 and 0 < yd < 9 and all_coords[y_axis[yd - 1]][x_axis[xd - 1]] is not None and all_coords[y_axis[yd - 1]][x_axis[xd - 1]].get_team() != team:
            moves.append(f'{x_axis[xd - 1]}{yd}')
    return moves

 
def Rook_movement(place: dict(), team: str(), all_coords: dict()):
    (x, y, moves) = (x_axis.index(place[0]), int(place[-1]) - 1, [])
    for xd in range(x - 1, -1, -1):
        if all_coords[y_axis[y]][x_axis[xd]] is None:
            moves.append(x_axis[xd] + y_axis[y])
        elif all_coords[y_axis[y]][x_axis[xd]] is not None and all_coords[y_axis[y]][x_axis[xd]].get_team() != team:
            moves.append(x_axis[xd] + y_axis[y])
            break
        elif all_coords[y_axis[y]][x_axis[xd]] is not None and all_coords[y_axis[y]][x_axis[xd]].get_team() == team: break
    for xd in range(x + 1, 8):
        if all_coords[y_axis[y]][x_axis[xd]] is None:
            moves.append(x_axis[xd] + y_axis[y])
        elif all_coords[y_axis[y]][x_axis[xd]] is not None and all_coords[y_axis[y]][x_axis[xd]].get_team() != team:
            moves.append(x_axis[xd] + y_axis[y])
            break
        elif all_coords[y_axis[y]][x_axis[xd]] is not None and all_coords[y_axis[y]][x_axis[xd]].get_team() == team: break
    for yd in range(y - 1, -1, -1):
        if all_coords[y_axis[yd]][x_axis[x]] is None:
            moves.append(x_axis[x] + y_axis[yd])
        elif all_coords[y_axis[yd]][x_axis[x]] is not None and all_coords[y_axis[yd]][x_axis[x]].get_team() != team:
            moves.append(x_axis[x] + y_axis[yd])
            break
        elif all_coords[y_axis[yd]][x_axis[x]] is not None and all_coords[y_axis[yd]][x_axis[x]].get_team() == team: break
    for yd in range(y + 1, 8):
        if all_coords[y_axis[yd]][x_axis[x]] is None:
            moves.append(x_axis[x] + y_axis[yd])
        elif all_coords[y_axis[yd]][x_axis[x]] is not None and all_coords[y_axis[yd]][x_axis[x]].get_team() != team:
            moves.append(x_axis[x] + y_axis[yd])
            break
        elif all_coords[y_axis[yd]][x_axis[x]] is not None and all_coords[y_axis[yd]][x_axis[x]].get_team() == team: break
    return moves
    

def Queen_movement(place: dict(), team: str(), all_coords: dict()):
    moves = Bishop_movement(place, team, all_coords) + Rook_movement(place, team, all_coords)
    return moves


def King_movement(place: dict(), team: str(), all_coords: dict()):
    (x, y, moves, newmoves) = (x_axis.index(place[0]), int(place[-1]) - 1, [], [])
    try: moves.append(x_axis[x - 1] + y_axis[y])
    except IndexError: pass
    try: moves.append(x_axis[x + 1] + y_axis[y])
    except IndexError: pass
    try: moves.append(x_axis[x] + y_axis[y - 1])
    except IndexError: pass
    try: moves.append(x_axis[x] + y_axis[y + 1])
    except IndexError: pass
    try: moves.append(x_axis[x - 1] + y_axis[y - 1])
    except IndexError: pass
    try: moves.append(x_axis[x - 1] + y_axis[y + 1])
    except IndexError: pass
    try: moves.append(x_axis[x + 1] + y_axis[y - 1])
    except IndexError: pass
    try: moves.append(x_axis[x - 1] + y_axis[y + 1])
    except IndexError: pass
    for item in moves:
        (x, y) = (x_axis.index(item[0]), int(item[-1]) - 1)
        if all_coords[y_axis[y]][x_axis[x]] is not None and all_coords[y_axis[y]][x_axis[x]].get_team() != team: newmoves.append(item)
    return newmoves


def check_shah(team: str(), kings_pos: dict(), attack_pos: str()):
    pass


def evaluate(board, team: str()):
    if team == 'black': return board.scores('black') - board.scores('white')
    else: return board.scores('white') - board.scores('black') 


def minimax(board, depth: int(), team: str()):
    if depth == 0: pass