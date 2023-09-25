from classModule import *
from os import system

def main():
    team_now = 'black'
    Running = True
    board = Board(First_realize())
    board.show()
    teamswaper = {'black': 'white', 'white': 'black'}
    
    movements = {
        'pawn': Pawn_movement,
        'bishop': Bishop_movement,
        'knight': Knight_movement,
        'rook': Rook_movement,
        'queen': Queen_movement,
        'king': King_movement
    }

    

    #print(board.get_figures_coords())
    print('Пример хода: a2 a4')

    while Running:
        
        if team_now == 'black': team_now = 'white'
        else: team_now = 'black'

        check = False
        cur_place, want = map(str, input('Ход команды {}: '.format(team_now)).split())
        while not check:
            check = not check
            if board.get_figures_coords()[cur_place[-1]][cur_place[0]] is None:
                cur_place, want = map(str, input('Невозможный ход, повторите попытку: ').split())
                check = not check
                continue
            if board.get_figures_coords()[cur_place[-1]][cur_place[0]].get_team() != team_now:
                cur_place, want = map(str, input('Невозможный ход, повторите попытку: ').split())
                check = not check
                continue
            if want not in movements[board.get_figure_type_on_place(cur_place)](cur_place, team_now, board.get_figures_coords()):             
                cur_place, want = map(str, input('Невозможный ход, повторите попытку: ').split())
                check = not check
                continue
        
        system('CLS')
        if board.swap(cur_place, want):
            board.show()
            print('Команда', team_now, "победила")
            Running = False
        else:
            board.show()
            if board.get_kings_position()[teamswaper[team_now]] in movements[board.get_figure_type_on_place(want)](want, team_now, board.get_figures_coords()):
                print('Вам шах')


    print('Игра окончена')


if __name__ == '__main__':
    main()