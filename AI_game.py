from classes import *
from AI_class import *

board = Board()
board.print_board('w')

bot=AI_simple(board,"b")


while not board.checkmated('w') and not board.checkmated('b'):
    print(board.all_possible_moves('w'))
    input_list=input("White move (from): ").split(",")
    x,y=int(input_list[0]),int(input_list[1])
    input_list=input("White move (to): ").split(",")
    new_x,new_y=int(input_list[0]),int(input_list[1])

    white_move=board.make_move((x,y),(new_x,new_y),'w')

    while not white_move:
        input_list=input("White move (from): ").split(",")
        x,y=int(input_list[0]),int(input_list[1])
        input_list=input("White move (to): ").split(",")
        new_x,new_y=int(input_list[0]),int(input_list[1])

        white_move=board.make_move((x,y),(new_x,new_y),'w')

    if board.checkmated('b'):
        break

    (x,y),(new_x,new_y)=bot.get_move()

    black_move=board.make_move((x,y),(new_x,new_y),'b')

    board.print_board('w')

board.print_board('w')
()
if board.checkmated('w'):
    print("Black wins")
else:
    print("White wins")
