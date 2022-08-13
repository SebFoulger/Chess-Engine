from abc import ABCMeta, abstractmethod, abstractclassmethod, ABC
from copy import deepcopy
from classes import *

class AI(ABC):

    def __init__(self,board :Board,team):
        self.board=board
        self.team=team

    def get_move(self):
        print(sorted(self.board.all_possible_moves(self.team),key=lambda x:self.evaluate_move(x),reverse=True))
        return sorted(self.board.all_possible_moves(self.team),key=lambda x:self.evaluate_move(x),reverse=True)[0]
    
    def evaluate_move(self,move):
        temp_board=deepcopy(self.board)
        temp_board.make_move(move[0],move[1],self.team)
        return self.heuristic(temp_board)

    def heuristic(self):
        pass
    

class AI_simple(AI):
    def __init__(self, board: Board, team):
        super().__init__(board,team)

    def heuristic(self, board):
        return board.evaluate_score(self.team)-board.evaluate_score({'b':'w','w':'b'}[self.team])
