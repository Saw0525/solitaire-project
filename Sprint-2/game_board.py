#game logic and board data

class GameBoard:

    def __init__(self):
        self.board = []
        self.size = 7

    def english_board(self):
        self.board = [
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,1,1,1,-1,-1],
        [1,1,1,1,1,1,1],
        [1,1,1,0,1,1,1],
        [1,1,1,1,1,1,1],
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,1,1,1,-1,-1]
    ]
        
    def hexagon_board(self):
        self.board = [
        [-1,-1,1,1,1,-1,-1],
        [-1,1,1,1,1,1,-1],
        [1,1,1,1,1,1,1],
        [1,1,1,0,1,1,1],
        [-1,1,1,1,1,1,-1],
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,-1,1,-1,-1,-1]
    ]
    
    def diamond_board(self):
        self.board = [
        [-1,-1,-1,1,-1,-1,-1],
        [-1,-1,1,1,1,-1,-1],
        [-1,1,1,1,1,1,-1],
        [1,1,1,0,1,1,1],
        [-1,1,1,1,1,1,-1],
        [-1,-1,1,1,1,-1,-1],
        [-1,-1,-1,1,-1,-1,-1]
    ]
    
    #new game function 
    def new_game(self, board_type):

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
                    if self.is_valid_move(r,c,r,c+2): return False
                    if self.is_valid_move(r,c,r,c-2): return False
                    if self.is_valid_move(r,c,r+2,c): return False
                    if self.is_valid_move(r,c,r-2,c): return False
                    
        return True
        
