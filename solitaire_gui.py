import tkinter as tk
from game_board import GameBoard, ManualMode, AutoMode #import from game board class following the case study : Tic Tac Toe

root = tk.Tk()
class SolitaireGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Solitaire")
        self.root.geometry("700x450")

        # left frame 
        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        
        tk.Label(left_frame, text="Board Type").grid(row=0,column=0)       
        ## radio buttons // Borad type to choose
        self.board_type = tk.StringVar(value="English")
        tk.Radiobutton(left_frame, text="English", variable=self.board_type, value="English",command=self.chang_board).grid(row=1,column=0,sticky="w")
        tk.Radiobutton(left_frame, text="Hexagon", variable=self.board_type, value="Hexagon",command=self.chang_board).grid(row=2,column=0,sticky="w")
        tk.Radiobutton(left_frame, text="Diamond", variable=self.board_type, value="Diamond",command=self.chang_board).grid(row=3,column=0,sticky="w")

        ##Game mode to choose
        tk.Label(left_frame, text="Game Mode").grid(row=6, column=0, pady=(10,0), sticky="w")
         
        #AI or manual 
        self.game_mode = tk.StringVar(value="Manual")
        tk.Radiobutton(left_frame, text="Manual", variable=self.game_mode, value="Manual").grid(row=7, column=0, sticky="w")
        tk.Radiobutton(left_frame, text="Auto", variable=self.game_mode, value="Auto").grid(row=8, column=0, sticky="w")

        #center frame
        # canvas for drawing board
        self.canvas = tk.Canvas(
            root,
            width=350,
            height=350,
            bg="#f4e7c5",
            highlightthickness=0
        )

        self.canvas.grid(row=0,column=1, padx=20, pady=20)
        
        #right frame
        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=2, padx=20, pady=20, sticky="n")
        #one board size for sprint2 // Later i plan to use the dropdown button for this with self.board_size
        self.board_size = tk.IntVar(value=7)
        tk.Label(right_frame, text= "Board Size:").grid(row=0, column=0, sticky="w")
        #dropdown for size
        tk.OptionMenu(right_frame, self.board_size, 5, 7, 9, 11).grid(row=0, column=1)


        # game logic
        self.game = None
        self.selected = None
        
         #start a new game
        tk.Button(right_frame, text="New Game", command=self.start_new_game).grid(row=1, column=0, columnspan=2, pady=10)
        #randomize
        tk.Button(right_frame, text="Randomize", command=self.randomize).grid(row=2, column=0, columnspan=2)
        #auto play
        tk.Button(right_frame, text="Autoplay", command=self.auto_play).grid(row=3, column=0, columnspan=2, pady=10)
      
        # draw the board
        self.draw_board()

        # detect mouse clicks
        self.canvas.bind("<Button-1>", self.handle_click)
             
               

    def draw_board(self):

        if self.game is None:
            self.canvas.create_text (175, 175, text="Select board and click New Game")
            return
        if not self.game.board.board:
            self.canvas.create_text(175, 175, text="Select board and click New Game")
            return

        self.canvas.delete("all")

        board = self.game.board.board
        size =  self.game.size
        
        rows = len(board)
        cols = len(board[0])

        board_width = cols * self.cell_size
        board_height = rows * self.cell_size
        self.x_offset = (350 - board_width) // 2
        self.y_offset = (350 - board_height) // 2

        for r in range(len(board)):
            for c in range(len(board[r])):

                value = board[r][c]

                if value == -1:
                    continue

                #x = c * self.cell_size + 30
                #y = r * self.cell_size + 30

                x = c * self.cell_size + self.x_offset + self.cell_size // 2
                y = r * self.cell_size + self.y_offset + self.cell_size // 2

                # draw hole
                self.canvas.create_oval(
                    x-14, y-14,
                    x+14, y+14,
                    fill="#d9c8a3",
                    outline=""
                )

                # draw peg
                if value == 1:
                    color = "#d94c3a"

                    if self.selected == (r,c):
                        color = "yellow"
                    self.canvas.create_oval(
                        x-11, y-11,
                        x+11, y+11,
                        fill=color,
                        outline="",
                        width=3)
    #Game over
    def show_game_over(self):
        self.canvas.create_text(175, 175, text= "Game Over", fill="red")
    # reset the game bt                     
    def start_new_game(self):
        
        board_type = self.board_type.get()
        size = self.board_size.get()
       
        #self.game.new_game(board_type, size)

        #Automatic or Manual
        if self.game_mode.get() == "Manual":
            self.game = ManualMode(board_type, size)
        else:
            self.game = AutoMode(board_type, size)
     
        # board display settings
        self.cell_size = 350 // self.game.size # to have board always fits
        self.peg_radius = 14

        self.cell_size = 350 // self.game.size
        self.selected=None
        self.draw_board()

        """if self.game_mode.get() == "Manual":
            self.randomize_loop()"""
        if self.game_mode.get() == "Auto":
            self.auto_play()


    #board selection to link with radio buttons
    def chang_board(self):
        if self.game is None:
            return # do nothin if there is no game 
        board_type = self.board_type.get()
        size = self.board_size.get()
        self.game.new_game(board_type, size)
        self.cell_size = 350 // self.game.size
        self.selected = None
        self.draw_board()

   
    #click peg and make moves
    def handle_click(self, event):
        ##clicks only work in manual mode
        if not isinstance(self.game, ManualMode):
            return
        ##can;t click
        if not self.game.board:
            return
         
        col = (event.x  - self.x_offset) // self.cell_size
        row = (event.y  - self.y_offset) // self.cell_size
        
        board = self.game.board.board

        #handle crashes if user clicks outsid the board
        if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
            return
        
        # first click → select peg
        if self.selected is None:
            
            if board[row][col] == 1:
                self.selected = (row, col)
                self.draw_board()

        # second click → attempt move
        else:
            r1, c1 = self.selected #previous selected peg
                
            moved = self.game.make_move(r1, c1, row, col)
            
            if moved:
                self.selected = None
                self.draw_board()
                #game over
                if self.game.game_over():
                    self.show_game_over()
            else:
                self.selected = None
                self.draw_board()
    #randomize function
    def randomize(self):
        self.game.randomize()
        self.draw_board()
    
    ## need to have peridodic randomization that the board randomize automically while playing
    def randomize_loop(self):
        if not isinstance(self.game, ManualMode):
            return  # only in manual mode

        self.game.randomize()
        self.draw_board()

        if not self.game.game_over():
            self.root.after(2000, self.randomize_loop)  # every 2 seconds
    ##auto play bt
    def auto_play(self):

        if not isinstance(self.game, AutoMode):
            return
         #make move
        moved = self.game.auto_move()
        self.draw_board()
        #no valid move then stop
        if not moved:
            self.show_game_over()
            return #stop the looop
        
        # repeat after delay
        self.root.after(500, self.auto_play)

        
app = SolitaireGUI(root)
root.mainloop()