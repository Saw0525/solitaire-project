#game logic and board data

import random


class GameBoard:

    def __init__(self, size = 7): # default size = 7
        self.board = []
        self.size = size
        
    def english_board(self):
            size = self.size
            self.board = []
            center = size // 2
            for r in range(size): 
                row = []
                for c in range(size):
                    if (r < center-1 or r > center+1) and (c < center-1 or c > center+1):
                        row.append(-1) # corner invalid
                    else:
                        row.append(1)
                    
                self.board.append(row)
            #empty center
            self.board[center][center]= 0  

    '''def english_board(self):
        self.board = [
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,1,1,1,-1,-1],
        [1,1,1,1,1,1,1],
        [1,1,1,0,1,1,1],
        [1,1,1,1,1,1,1],
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,1,1,1,-1,-1]
    ]'''       

        
    def hexagon_board(self):
        size = self.size
        center = size // 2
        self.board = []

        for r in range(size):
            row = []

            for c in range(size):
                # THIS is the correct condition
                if (abs(r - center) <= center and
                    abs(c - center) <= center and
                    abs(r - center) + abs(c - center) <= center + center//2):
                    row.append(1)
                else:
                    row.append(-1)

            self.board.append(row)

        self.board[center][center] = 0 

    '''def hexagon_board(self):
        self.board = [
        [-1,-1,1,1,1,-1,-1],
        [-1,1,1,1,1,1,-1],
        [1,1,1,1,1,1,1],
        [1,1,1,0,1,1,1],
        [1,1,1,1,1,1,1],
        [-1,1,1,1,1,1,-1],
        [-1,-1,1,1,1,-1,-1]
        
    ]'''
    def diamond_board(self):
            size = self.size
            self.board = []
            center = size // 2
            for r in range(size): 
                row = []
                for c in range(size):
                    if abs(r - center) + abs(c - center) <= center:
                        row.append(1) # valid
                    else:
                        row.append(-1) #invalid
                    
                self.board.append(row)
            #empty center
            self.board[center][center]= 0  
    '''def diamond_board(self):
        self.board = [
        [-1,-1,-1,1,-1,-1,-1],
        [-1,-1,1,1,1,-1,-1],
        [-1,1,1,1,1,1,-1],
        [1,1,1,0,1,1,1],
        [-1,1,1,1,1,1,-1],
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,-1,1,-1,-1,-1]
    ]'''
    
    #new game function 
    def new_game(self, board_type, size):
        self.size = size

        if board_type == "English":
            self.english_board()
        elif board_type =="Hexagon":
            self.hexagon_board()
        elif board_type == "Diamond":
            self.diamond_board()


    
    def get_cell(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        return -1
    
    def is_valid_move(self, r1, c1, r2, c2):
        if self.get_cell(r1,c1) != 1:
            return False
        
        if self.get_cell(r2,c2) != 0:
            return False
        if r1 == r2 and abs(c1-c2) == 2:
            mid = (c1+c2)//2
            return self.get_cell(r1,mid) == 1
        if c1 == c2 and abs(r1-r2) == 2:
            mid = (r1+r2)//2
            return self.get_cell(mid,c1) == 1
        return False
    
    def make_move(self, r1, c1, r2, c2):
        if self.is_valid_move(r1,c1,r2,c2):
            mid_r = (r1+r2)//2
            mid_c = (c1+c2)//2
            self.board[r1][c1] = 0
            self.board[mid_r][mid_c] = 0
            self.board[r2][c2] = 1
            return True
        return False
    
    def game_over(self):
        for r in range(self.size):
            for c in range(self.size):
                
                if self.board[r][c] == 1:

                    directions = [(0,2), (0,-2), (2,0), (-2,0)]
                    for dr, dc in directions:
                        r2 = r + dr
                        c2 = c + dc
                        if 0 <= r2 < self.size and 0 <= c2 < self.size:
                            if self.is_valid_move(r, c, r2, c2):
                                return False   # move exists → not game over
                    
        return True
    #randomize board
    def randomize(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != -1:
                    self.board[r][c] = random.choice([0, 1])
        #set center
        center = self.size // 2
        self.board[center][center] = 0

    #automated game mode
    def auto_move(self):

        import random
        moves = []
        for r in range(self.size):
            for c in range(self.size):

                if self.board[r][c] == 1:

                    directions = [(0,2), (0,-2), (2,0), (-2,0)]

                    for dr, dc in directions:
                        r2 = r + dr
                        c2 = c + dc

                        if 0 <= r2 < self.size and 0 <= c2 < self.size:
                            if self.is_valid_move(r, c, r2, c2):
                                moves.append((r, c, r2, c2)) # become one object/a tuple
         #pick random move                       
        if moves:
                move = random.choice(moves)
                self.make_move(*move)
                return True

        return False   # no move found
    
#Class Hierarchy
class SolitaireGame:
    def __init__(self, board_type, size):
        self.board = GameBoard(size)
        self.board.new_game(board_type, size)
        self.size = size

    def game_over(self):
        return self.board.game_over()

    def randomize(self):
        self.board.randomize()


class ManualMode(SolitaireGame):
    def make_move(self, r1, c1, r2, c2):
        return self.board.make_move(r1, c1, r2, c2)


class AutoMode(SolitaireGame):
    def auto_move(self):
        return self.board.auto_move()