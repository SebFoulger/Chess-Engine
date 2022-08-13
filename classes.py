
from copy import copy, deepcopy

def long_moves(piece,temp_list, max_length=8):
    temp_moves=[]
    for change in temp_list:
        x=piece.position[0]+change[0]
        y=piece.position[1]+change[1]
        while y<8 and y>=0 and x<8 and x>=0 and abs(x-piece.position[0])<=max_length and abs(y-piece.position[1])<=max_length:
            if piece.board.get_piece((x,y),piece.team)==None:
                temp_moves.append((x,y))
            elif piece.board.get_piece((x,y),piece.team).get_team()!=piece.team:
                temp_moves.append((x,y))
                break
            else:
                break
            y+=change[1]
            x+=change[0]
    return temp_moves

def king_not_targeted(temp_moves, piece):
    temp_moves=temp_moves.copy()

    i=0
    while i<len(temp_moves):
        temp_board=deepcopy(piece.board)
        move=temp_moves[i]
        temp_piece=temp_board.get_piece(piece.position,piece.team)
        temp_piece.set_pos(move)
        if temp_board.kings[['w','b'].index(piece.team)].in_target():
            temp_moves.pop(i)
        else:
            i+=1

    return temp_moves

class Move:
    def __init__(self, moved_piece_name,old_position,new_position, team):
        self.moved_piece_name=moved_piece_name
        self.old_position=old_position
        self.new_position=new_position
        self.team=team
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Board:
    def __init__(self, pieces=[], move_history=[], most_recent_move= Move(" ",(-1,-1),(-1,-1),'w'), taken=[[],[]], current_pieces=[],kings=[]):
        if pieces==[]:
            #Initialise chess board
            white_pieces=[]

            empty_row=[]
            for i in range(0, 8):
                empty_row.append(None)
            
            # First row:
            first_row=[Rook(self,'w',(0,0)),Knight(self,'w',(1,0)),Bishop(self,'w',(2,0)),Queen(self,'w',(3,0)),King(self,'w',(4,0)),Bishop(self,'w',(5,0)),Knight(self,'w',(6,0)),Rook(self,'w',(7,0))]

            white_pieces.append(first_row)

            # Second row:
            second_row=[]
            for i in range(0,8):
                second_row.append(Pawn(self,'w',(i,1)))
            white_pieces.append(second_row)

            # Empty rows:
            for i in range(2,8):
                white_pieces.append(empty_row)

            black_pieces=[]
            self.current_pieces=[first_row[:4]+first_row[5:]+second_row]
            self.kings=[first_row[4]]

            # First row:
            first_row=[Rook(self,'b',(0,0)),Knight(self,'b',(1,0)),Bishop(self,'b',(2,0)),King(self,'b',(3,0)),Queen(self,'b',(4,0)),Bishop(self,'b',(5,0)),Knight(self,'b',(6,0)),Rook(self,'b',(7,0))]
            black_pieces.append(first_row)

            # Second row:
            second_row=[]
            for i in range(0,8):
                second_row.append(Pawn(self,'b',(i,1)))
            black_pieces.append(second_row)

            # Empty rows:
            for i in range(2,8):
                black_pieces.append(empty_row)
            white_pieces=list(map(list, zip(*white_pieces)))
            black_pieces=list(map(list, zip(*black_pieces)))
            self.pieces=[white_pieces,black_pieces]

            self.current_pieces.append(first_row[:3]+first_row[4:]+second_row)
            self.kings.append(first_row[3])
        else:
            self.pieces=pieces
            self.current_pieces=current_pieces
            self.kings=kings
        self.move_history=move_history
        self.most_recent_move=most_recent_move
        # taken stores [pieces that white has taken,pieces that black has taken]
        self.taken = taken
        

    def get_piece(self, position, move_team):
        if position[0]<0 or position[0]>7 or position[1]<0 or position[1]>7:
            return None
        elif move_team=='w':
            if self.pieces[0][position[0]][position[1]]!=None:
                return self.pieces[0][position[0]][position[1]]
            elif self.pieces[1][7-position[0]][7-position[1]]!=None:
                return self.pieces[1][7-position[0]][7-position[1]]
            elif self.kings[0].position==(position[0],position[1]):
                return self.kings[0]
            elif self.kings[1].position==(7-position[0],7-position[1]):
                return self.kings[1]
        else: 
            if self.pieces[0][7-position[0]][7-position[1]]!=None:
                return self.pieces[0][7-position[0]][7-position[1]]
            elif self.pieces[1][position[0]][position[1]]!=None:
                return self.pieces[1][position[0]][position[1]]
            elif self.kings[1].position==(position[0],position[1]):
                return self.kings[1]
            elif self.kings[0].position==(7-position[0],7-position[1]):
                return self.kings[0]
        return None

    def move_piece(self,old_position,new_position,move_team):

        taken_piece=self.get_piece(new_position,move_team)
        moving_piece=self.get_piece(old_position,move_team)
        
        atk_team=moving_piece.get_team()
        if taken_piece!=None and not isinstance(taken_piece,King):
            self.taken[['w','b'].index(atk_team)].append(taken_piece)
            
            self.current_pieces[['b','w'].index(atk_team)].remove(taken_piece)
        elif self.get_piece((new_position[0],new_position[1]-1),move_team)!=None: # En passant special case:
            if moving_piece.name=='P' and self.get_piece((new_position[0],new_position[1]-1),move_team).name=='P' and new_position[0]!=old_position[0]:
                self.taken[['w','b'].index(atk_team)].append(self.get_piece((new_position[0],new_position[1]-1),move_team))
                self.current_pieces[['b','w'].index(atk_team)].remove(self.get_piece((new_position[0],new_position[1]-1),move_team))
                self.pieces[['b','w'].index(atk_team)][7-(new_position[0])][7-(new_position[1]-1)]=None
        elif moving_piece.name=="K" and old_position[0]-new_position[0]==2: # Castling left
            self.get_piece((0,0),atk_team).set_pos((new_position[0]+1,new_position[1]))
        elif moving_piece.name=="K" and old_position[0]-new_position[0]==-2: # Castling right
            self.get_piece((7,0),atk_team).set_pos((new_position[0]-1,new_position[1]))


        
        self.pieces[['w','b'].index(atk_team)][new_position[0]][new_position[1]]=moving_piece
        self.pieces[['w','b'].index(atk_team)][old_position[0]][old_position[1]]=None
        self.pieces[['b','w'].index(atk_team)][7-new_position[0]][7-new_position[1]]=None


        self.move_history.append(Move(moving_piece.name,old_position,new_position,moving_piece.get_team()))
        self.most_recent_move=Move(moving_piece.name,old_position,new_position,moving_piece.get_team())
    
    def make_move(self,old_position,new_position,move_team):
        moving_piece=self.get_piece(old_position,move_team)
        if moving_piece==None:
            return False
        elif new_position not in moving_piece.get_possible_moves():
            return False
        else:
            moving_piece.set_pos(new_position)
            return True



    def exchange_pawn(self,position,move_team,replace_with):
        pawn_to_replace = self.get_piece(position,move_team)
        assert pawn_to_replace.get_pos()[1]==7
        
        self.pieces[['w','b'].index(pawn_to_replace.get_team())][position[0]][position[1]]=replace_with #Placeholder
        self.current_pieces[['w','b'].index(pawn_to_replace.get_team())].remove(pawn_to_replace)
        self.current_pieces[['w','b'].index(pawn_to_replace.get_team())].append(replace_with)

    def evaluate_score(self,team):
        cur_score=0
        for piece in self.current_pieces[['w','b'].index(team)]:
            cur_score+=piece.score
        
        return cur_score
    
    def checkmated(self,team):
        if len(self.kings[['w','b'].index(team)].get_possible_moves())!=0:
            return False
        for piece in self.current_pieces[['w','b'].index(team)]:
            if len(piece.get_possible_moves())!=0:
                return False
        
        return True

    def all_possible_moves(self,team):
        temp_moves=[]
        for piece in self.current_pieces[['w','b'].index(team)]:
            temp_moves=temp_moves+(list(map(lambda x: (piece.position,x),piece.get_possible_moves(True))))
        temp_moves=temp_moves+list(map(lambda x: (piece.position,x),self.kings[['w','b'].index(team)].get_possible_moves(True)))
        return temp_moves

    def print_board(self, perspective):
        symbol_dict={'wP':'♙','wR':'♖','wKn':'♘','wB':'♗','wK':'♔','wQ':'♕','bP':'♟','bR':'♜','bKn':'♞','bB':'♝','bK':'♚','bQ':'♛'}
        total_board=[]
        for i in range(8):
            temp=[]
            for j in range(8):
                if self.pieces[0][j][i]!=None:
                    temp.append(self.pieces[0][j][i])
                elif self.pieces[1][7-j][7-i]!=None:
                    temp.append(self.pieces[1][7-j][7-i])
                else:
                    temp.append(None)
            total_board.append(temp)
        output_list=[]
        output_list.append('   -- -- -- -- -- -- -- -- ')
        for i in range(len(total_board)):
            temp_str=str(i)+' |'
            for j in total_board[i]:
                #Fill in other pieces
                if isinstance(j,Piece):
                    temp_str+=''+symbol_dict[j.get_team()+j.name]+' |' 
                else:
                    temp_str+='  |'
            output_list.append(temp_str)
            output_list.append('   -- -- -- -- -- -- -- -- ')
        if perspective=='w':
            output_list.reverse()
        if perspective=='b':
            for i in range(len(output_list)):
                output_list[i]=output_list[i][::-1]
        output_list.append('   0  1  2  3  4  5  6  7  ')
        for i in output_list:
            print(i)
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Piece:
    
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        assert isinstance(new_board,Board)
        assert new_team=='w' or new_team=='b'
        assert isinstance(new_position,tuple)
        assert isinstance(new_position[0],int) and isinstance(new_position[1],int)
        assert new_position[0]>=0 and new_position[0]<=7 and new_position[1]>=0 and new_position[0]<=7
        self.board=new_board
        self.team=new_team
        self.position=new_position
        self.initial_pos=new_position
        self.has_moved=has_moved


    def get_pos(self):
        return self.position

    def get_team(self):
        return self.team

    def hard_set_pos(self,new_pos):
        self.position=new_pos
        self.has_moved=True

    def set_pos(self,new_pos):
        self.board.move_piece(self.position,new_pos, self.team)
        self.position=new_pos
        self.has_moved=True

    def in_target(self):
        for piece in self.board.current_pieces[['b','w'].index(self.team)]:
            for move in piece.get_possible_moves(check_bool=False):
                if self.position==(7-move[0],7-move[1]) and not (isinstance(piece,Pawn) and move[0]==piece.position[0]):
                    return True
        return False
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Pawn(Piece):
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        super().__init__(new_board,new_team, new_position, has_moved)
        self.name="P"
        self.score=1
        

    def get_possible_moves(self, check_bool=True):
        temp_moves=[]

        # Move forwards 1:
        if self.position[1]<7:
            if self.board.get_piece((self.position[0],self.position[1]+1),self.team)==None and self.board.get_piece((7-self.position[0],7-self.position[1]-1),{'w':'b','b':'w'}[self.team])==None:
                temp_moves.append((self.position[0],self.position[1]+1))
            
            # Move forwards 2:
            if self.position[1]<6:
                if self.board.get_piece((self.position[0],self.position[1]+2),self.team)==None and self.board.get_piece((self.position[0],self.position[1]+1),self.team)==None and not self.has_moved and self.board.get_piece((7-self.position[0],7-self.position[1]-2),{'w':'b','b':'w'}[self.team])==None and self.board.get_piece((7-self.position[0],7-self.position[1]-1),{'w':'b','b':'w'}[self.team])==None:
                    temp_moves.append((self.position[0],self.position[1]+2))
            
            # Take up right
            if self.position[0]<7:
                if isinstance(self.board.get_piece((self.position[0]+1,self.position[1]+1),self.team),Piece):
                    if self.board.get_piece((self.position[0]+1,self.position[1]+1),self.team).get_team()!=self.team:
                        temp_moves.append((self.position[0]+1,self.position[1]+1))
            
            # Take up left
            if self.position[0]>0:
                if isinstance(self.board.get_piece((self.position[0]-1,self.position[1]+1),self.team),Piece):
                    if self.board.get_piece((self.position[0]-1,self.position[1]+1),self.team).get_team()!=self.team:
                        temp_moves.append((self.position[0]-1,self.position[1]+1))

            # En passant up right
            if self.board.most_recent_move.moved_piece_name=='P' and abs(self.board.most_recent_move.new_position[1]-self.board.most_recent_move.old_position[1])==2 and self.position[0]-(7-self.board.most_recent_move.old_position[0])==-1 and self.position[1]==4:
                temp_moves.append((self.position[0]+1,self.position[1]+1))

            # En passant up left
            if self.board.most_recent_move.moved_piece_name=='P' and abs(self.board.most_recent_move.new_position[1]-self.board.most_recent_move.old_position[1])==2 and self.position[0]-(7-self.board.most_recent_move.old_position[0])==1 and self.position[1]==4:
                temp_moves.append((self.position[0]-1,self.position[1]+1))
        if check_bool:
            temp_moves=king_not_targeted(temp_moves,self)


        return temp_moves

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Rook(Piece):
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        super().__init__(new_board,new_team, new_position, has_moved)
        self.name="R"
        self.score=5
    
    def get_possible_moves(self, check_bool=True):
        # Note castling will be implemented in the king class
        temp_moves=long_moves(self,[(1,0),(-1,0),(0,1),(0,-1)])
        if check_bool:
            temp_moves=king_not_targeted(temp_moves,self)
        return temp_moves

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Bishop(Piece):
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        super().__init__(new_board,new_team, new_position, has_moved)
        self.name="B"
        self.score=3

    
    def get_possible_moves(self, check_bool=True):
        temp_moves=long_moves(self,[(1,1),(-1,1),(1,-1),(-1,-1)])
        if check_bool:
            temp_moves=king_not_targeted(temp_moves,self)
        return temp_moves


    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Queen(Piece):
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        super().__init__(new_board,new_team, new_position, has_moved)
        self.name="Q"
        self.score=9

    
    def get_possible_moves(self, check_bool=True):
        temp_moves=long_moves(self,[(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)])
        if check_bool:
            temp_moves=king_not_targeted(temp_moves,self)
        return temp_moves

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class Knight(Piece):
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        super().__init__(new_board,new_team, new_position, has_moved)
        self.name="Kn"
        self.score=3

    def get_possible_moves(self, check_bool=True):
        temp_moves=[]

        poss_moves=[(1,2),(2,1),(1,-2),(-2,1),(-1,2),(2,-1),(-1,-2),(-2,-1)]

        for move in poss_moves:
            cur_move=(self.position[0]+move[0],self.position[1]+move[1])
            if cur_move[0]<8 and cur_move[0]>=0 and cur_move[1]<8 and cur_move[1]>=0:
                if self.board.get_piece(cur_move,self.team)==None or self.board.get_piece(cur_move,self.team).get_team()!=self.team:
                    temp_moves.append(cur_move)


        
        if check_bool:
            temp_moves=king_not_targeted(temp_moves,self)
        return temp_moves

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

class King(Piece):
    def __init__(self, new_board, new_team, new_position, has_moved=False):
        super().__init__(new_board,new_team, new_position, has_moved)
        self.name="K"
        self.score=1000
    
    def get_possible_moves(self, check_bool=True):
        temp_moves=[]

        # Castle left:
        empty_between=True
        for i in range(1,self.position[0]):
            empty_between=empty_between and (self.board.get_piece((i,self.position[1]),self.team)==None) and not King(self.board,self.team,(i,self.position[1])).in_target()

        if empty_between and not self.has_moved and self.board.get_piece((0,0),self.team)!=None and not self.in_target(): 
            if not self.board.get_piece((0,0),self.team).has_moved:
                temp_moves.append((self.position[0]-2,self.position[1]))
        
        # Castle right:
        empty_between=True
        for i in range(self.position[0]+1,7):
            empty_between=empty_between and (self.board.get_piece((i,self.position[1]),self.team)==None) and not King(self.board,self.team,(i,self.position[1])).in_target()

        if empty_between and not self.has_moved and self.board.get_piece((7,0),self.team)!=None and not self.in_target(): 
            if not self.board.get_piece((7,0),self.team).has_moved:
                temp_moves.append((self.position[0]+2,self.position[1]))

        for move in long_moves(self,[(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)], max_length=1):
            if not King(self.board,self.team,move).in_target():
                temp_moves.append(move)
        if check_bool:
            temp_moves=king_not_targeted(temp_moves,self)
        return temp_moves
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
