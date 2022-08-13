from classes import *

board = Board()
board.print_board('w')

while not board.checkmated('w') and not board.checkmated('b'):
    print(board.evaluate_score('w'))
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

    board.print_board('b')
    if board.checkmated('b'):
        break

    input_list=input("Black move (from): ").split(",")
    x,y=int(input_list[0]),int(input_list[1])
    input_list=input("Black move (to): ").split(",")
    new_x,new_y=int(input_list[0]),int(input_list[1])

    black_move=board.make_move((x,y),(new_x,new_y),'b')

    while not black_move:
        input_list=input("Black move (from): ").split(",")
        x,y=int(input_list[0]),int(input_list[1])
        input_list=input("Black move (to): ").split(",")
        new_x,new_y=int(input_list[0]),int(input_list[1])

        black_move=board.make_move((x,y),(new_x,new_y),'b')

    board.print_board('w')
    
board.print_board('w')
()
if board.checkmated('w'):
    print("Black wins")
else:
    print("White wins")
