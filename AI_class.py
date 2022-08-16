from abc import ABCMeta, abstractmethod, abstractclassmethod, ABC
from copy import deepcopy
from classes import *
import random
from itertools import groupby

class AI(ABC):

    def __init__(self,board :Board,team):
        self.board=board
        self.team=team

    def get_move(self):
        pass     
    
    def evaluate_move(self,move):
        temp_board=deepcopy(self.board)
        temp_board.make_move(move[0],move[1],self.team)
        return self.heuristic(temp_board)

    def get_move(self):

        return sorted(self.board.all_possible_moves(self.team), key=lambda x:self.evaluate_move(x), reverse=True)[0]

    def heuristic(self):
        pass
class AI_random(AI):

    def __init__(self,board :Board,team):
        super().__init__(board,team)

    def get_move(self):
        
        possible_moves=self.board.all_possible_moves(self.team)
        moves_scores=sorted(map(lambda x:(x,self.evaluate_move(x)),possible_moves),key=lambda x:x[1],reverse=True)
        print(moves_scores)
        temp=list(next(groupby(moves_scores,lambda x:x[1]))[1])
        return temp[random.randint(0,len(temp)-1)][0]

class AI_simple(AI_random):
    def __init__(self, board: Board, team):
        super().__init__(board,team)
    
    # One step max score difference heuristic (prioritise checkmate)
    def heuristic(self, board):
        if board.checkmated(self.team):
            return -2**10
        if board.checkmated({'b':'w','w':'b'}[self.team]):
            return 2**10
        return board.evaluate_score(self.team)-board.evaluate_score({'b':'w','w':'b'}[self.team])

class AI_1step_minimax(AI_random):
    def __init__(self, board: Board, team):
        super().__init__(board,team)
    
    # n step max score difference heuristic (prioritise checkmate)
    def heuristic(self, board):
        if board.checkmated(self.team):
            return -2**10
        if board.checkmated({'b':'w','w':'b'}[self.team]):
            return 2**10
        
        cur_score=2**8
        for other_move in board.all_possible_moves({'b':'w','w':'b'}[self.team]):
            temp_board=deepcopy(board)
            temp_board.make_move(other_move[0],other_move[1],{'b':'w','w':'b'}[self.team])
            if temp_board.checkmated(self.team):
                cur_score=-2**10
            elif temp_board.evaluate_score(self.team)-temp_board.evaluate_score({'b':'w','w':'b'}[self.team])<cur_score:
                cur_score=temp_board.evaluate_score(self.team)-temp_board.evaluate_score({'b':'w','w':'b'}[self.team])   

        return cur_score