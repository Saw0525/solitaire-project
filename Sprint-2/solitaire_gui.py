import tkinter as tk
from game_board import GameBoard #import from game board class following the case study : Tic Tac Toe

root = tk.Tk()
class SolitaireGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Solitaire")
        self.root.geometry("600x450")

        # game logic
        self.game = GameBoard()
        self.selected = None
        self.game.new_game("English")

         #start a new game
        self.new_gamebt = tk.Button(
            root,
            text = "New Game",
            command=self.start_new_game
        )
        self.new_gamebt.grid(row=2, column=1)

        # board display settings
        self.cell_size = 40
        self.peg_radius = 14

        # canvas for drawing board
        self.canvas = tk.Canvas(
            root,
            width=350,
            height=350,
            bg="#f4e7c5",
            highlightthickness=0
        )

        self.canvas.grid(row=1, column=1, padx=20, pady=20)

        # draw the board
        self.draw_board()

        # detect mouse clicks
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Left panel
        board_frame = tk.Frame(root)
        board_frame.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        tk.Label(board_frame, text="Board Type").grid(row=0,column=0)

       
        ## radio buttons
        self.board_type = tk.StringVar(value="English")
        tk.Radiobutton(board_frame, text="English", variable=self.board_type, value="English",command=self.chang_board).grid(row=1,column=0,sticky="w")
        tk.Radiobutton(board_frame, text="Hexagon", variable=self.board_type, value="Hexagon",command=self.chang_board).grid(row=2,column=0,sticky="w")
        tk.Radiobutton(board_frame, text="Diamond", variable=self.board_type, value="Diamond",command=self.chang_board).grid(row=3,column=0,sticky="w")

        #one board size for sprint2 // Later i plan to use the dropdown button for this with self.board_size
        self.board_size = tk.StringVar(value="7")
        tk.Label(root, text= "Board Size: 7").grid(row=0, column=2)

       

    def draw_board(self):

        self.canvas.delete("all")

        board = self.game.board
        rows = len(board)
        cols = len(board[0])

        board_width = cols * self.cell_size
        board_height = rows * self.cell_size
        x_offset = (350 - board_width) // 2
        y_offset = (350 - board_height) // 2

        for r in range(len(board)):
            for c in range(len(board[r])):

                value = board[r][c]

                if value == -1:
                    continue

                #x = c * self.cell_size + 30
                #y = r * self.cell_size + 30

                x = c * self.cell_size + x_offset
                y = r * self.cell_size + y_offset

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

    # reset the game bt                     
    def start_new_game(self):
        board_type = self.board_type.get()
        self.game.new_game(board_type)
        self.selected=None
        self.draw_board()

    #board selection to link with radio buttons
    def chang_board(self):
        board_type = self.board_type.get()
        self.game.new_game(board_type)
        self.selected = None
        self.draw_board()

    #click peg and make moves
    def handle_click(self, event):
                    
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        board = self.game.board

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
            r1, c1 = self.selected
                
            moved = self.game.make_move(r1, c1, row, col)
            
            if moved:
                self.selected = None
                self.draw_board()
                #game over
                if self.game.game_over():
                    print("Game Over")
            else:
                self.selected = None
                self.draw_board()

        
app = SolitaireGUI(root)
root.mainloop()