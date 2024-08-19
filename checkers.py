"""
checkers.py

A simple checkers engine written in Python with the pygame 1.9.1 libraries.

Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm

I adapted some code from checkers.py found at 
http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py starting on line 159 of my program.

This is the final version of my checkers project for Programming Workshop at Marlboro College. The entire thing has been rafactored and made almost completely object oriented.

Funcitonalities include:

- Having the pieces and board drawn to the screen

- The ability to move pieces by clicking on the piece you want to move, then clicking on the square you would
  like to move to. You can change you mind about the piece you would like to move, just click on a new piece of yours.

- Knowledge of what moves are legal. When moving pieces, you'll be limited to legal moves.

- Capturing

- DOUBLE capturing etc.

- Legal move and captive piece highlighting

- Turn changes

- Automatic kinging and the ability for them to move backwords

- Automatic check for and end game. 

- A silky smoooth 60 FPS!

Everest Witman - May 2014 - Marlboro College - Programming Workshop 
"""

import pygame, sys
from pygame.locals import *
import numpy as np
pygame.font.init()
import time

##COLORS##
#            R    G    B 
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Game:
	"""
	The main game control.
	"""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		self.board_string=self.board.board_piece_string(self.board.matrix)
		print(self.board_string)		
		self.turn = BLUE
		self.selected_piece = None # a board location. 
		self.hop = False
		self.selected_legal_moves = []

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

	def minimax_decision(self,board_string):
		"""This method is what you will call to decide the best move for MAX
		   The function should return two things a piece on the board that is RED a valid move
		   I have written this function to make a call to MIN (min_value) which will return its utility after calling MAX (max_value)
		   The implementation is designed to work with alpha beta pruning and a depth cutoff, you are allowed to modify this implementation
		   If you are going to modify this function explain in your documentation what you are doing and how this is supposed to work.
		"""
		
		my_piece_locations=self.get_my_pieces(board_string)
		input_board=Board(board_string)
		move=None
		piece=None
		curr_utility=-float("inf")
		considered_locations=[]
		for location in my_piece_locations:
			if len(input_board.legal_moves(location))>0:
				considered_locations.append(location)		
		for location in considered_locations:
			valid_moves=input_board.legal_moves(location)
			for valid_move in valid_moves:
				copy_board=Board(input_board.board_piece_string(input_board.matrix))
				alpha=-float("inf")
				beta=float("inf")
				copy_board.move_piece(location,valid_move)
				if valid_move not in copy_board.adjacent(location):
					copy_board.remove_piece(((location[0] + valid_move[0]) >> 1, (location[1] + valid_move[1]) >> 1))
				utility=self.min_value(copy_board.board_piece_string(copy_board.matrix),alpha,beta,cutoff=5)
				'''
				The below two lines are for this code to work without breaking
				You just return the first location and the first valid move
				'''
				if utility is None:
					return location,valid_move
				if utility > curr_utility:
					curr_utility=utility
					piece=location
					move=valid_move
		return piece,move
	
	def get_my_pieces(self,board_string,color='R'):
		'''
			Returns the locations of your pieces
			you need to pass the board string and the appropriate color
		'''
		locations=np.argwhere(board_string==color)
		locations2=np.argwhere(board_string==color+"K")
		if locations2.shape[0] > 0:
			return np.concatenate((locations,locations2),axis=0)
		return locations
	
	def min_value(self,board_string,alpha,beta,cutoff):	
		'''
		This is the MIN implementation
		You will have to return the best possible utility for MIN 
		given the current conditions
		'''
		v = float("inf")

		considered_locations=[]

		input_board=Board(board_string) #Create the original board to save it.

		if cutoff == 0:
			return self.evaluation_function(input_board.board_piece_string(input_board.matrix))
		
		cutoff = cutoff-1
		
		my_piece_locations=self.get_my_pieces(board_string) #What are my current pieces in my board
		
		for location in my_piece_locations: #Get me all my pieces
			if len(input_board.legal_moves(location))>0:
				considered_locations.append(location)

		for location in considered_locations: #For every piece I have, what are its legal moves?
			valid_moves=input_board.legal_moves(location)
		
			if not valid_moves: #Terminal test if no moves possible
				return self.evaluation_function(input_board.board_piece_string(input_board.matrix))

			for valid_move in valid_moves: #For every legal move: 
				copy_board=Board(input_board.board_piece_string(input_board.matrix))

				copy_board.move_piece(location,valid_move) #Using the copy of the board, perform the corresponding move.
				if valid_move not in copy_board.adjacent(location): #Remove the piece if the move correspondes to taking a piece.
					copy_board.remove_piece(((location[0] + valid_move[0]) >> 1, (location[1] + valid_move[1]) >> 1))
				
				v = min(v, self.max_value(copy_board.board_piece_string(copy_board.matrix),alpha, beta, cutoff))

				if v <= alpha:
					return v
				
				beta = min(v, beta)

		return v

	def max_value(self,board_string,alpha,beta,cutoff):
		'''
		This is the MAX implementation
		You will have to return the best possible utility for MAX 
		given the current conditions
		'''
		v = -float("inf")

		considered_locations=[]

		input_board=Board(board_string) #Create the original board to save it.
		my_piece_locations=self.get_my_pieces(board_string) #What are my current pieces in my board

		if cutoff == 0:
			return self.evaluation_function(input_board.board_piece_string(input_board.matrix))
		
		cutoff = cutoff-1

		for location in my_piece_locations: #Get me all my pieces
			if len(input_board.legal_moves(location))>0:
				considered_locations.append(location)

		for location in considered_locations: #For every piece I have, what are its legal moves?
			valid_moves=input_board.legal_moves(location)
		
			if not valid_moves: #Terminal test
				return self.evaluation_function(input_board.board_piece_string(input_board.matrix))
			
			for valid_move in valid_moves: #For every legal move: 
				copy_board=Board(input_board.board_piece_string(input_board.matrix))

				copy_board.move_piece(location,valid_move) #Using the copy of the board, perform the corresponding move.

				if valid_move not in copy_board.adjacent(location): #Remove the piece if the move correspondes to taking a piece.
					copy_board.remove_piece(((location[0] + valid_move[0]) >> 1, (location[1] + valid_move[1]) >> 1))
				
				v = max(v, self.min_value(copy_board.board_piece_string(copy_board.matrix),alpha, beta, cutoff))

				if v >= beta:
					return v
			
			alpha = max(v, alpha)

		return v
	
	def evaluation_function(self,board_string):
		'''
		This is the evaluation function
		This is a naive implementation it returns the weighted number of pieces between RED (MAX) and BLUE (MIN)
		The evaluation function returns the appropriate value for MIN and MAX for them to optimize
		You have to modify the evaluation function as you find appropriate
		'''
		# Total amount of pieces at the start of the game / number of pieces that are currently on the board
		# Multiply by the weighted difference

		current_pieces = len(self.get_my_pieces(board_string, color = "R")) + len(self.get_my_pieces(board_string, color = "B"))
		start_of_game_pieces = 24

		weighted_difference = (len(np.argwhere(board_string=='R').tolist()) + len(np.argwhere(board_string=='RK').tolist())*2 ) -\
			  (len(np.argwhere(board_string=='B').tolist()) + len(np.argwhere(board_string=='BK').tolist())*2 )
		
		return (start_of_game_pieces / current_pieces) * weighted_difference
	
	def event_loop(self):
		"""
		The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state.
		"""
		if self.turn != BLUE:
			'''
			This is where minimax_decision is called
			You will not need to make any changes to the logic here
			'''
			selected_piece,move_position=self.minimax_decision(self.board_string)
			if selected_piece is None or move_position is None:
				'''
				This should not be reached unless RED has no valid moves
				'''
				self.end_turn()
			else:
				self.board.move_piece(selected_piece,move_position)

				if move_position not in self.board.adjacent(selected_piece):
					self.board.remove_piece(((selected_piece[0] + move_position[0]) >> 1, (selected_piece[1] + move_position[1]) >> 1))
				self.end_turn()
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?	
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

		for event in pygame.event.get():
			if event.type == QUIT:
				self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:
				# Detect mouse down first and paint legal moves
				# If the next mouse down happens and you have a selected piece and the mouse down is legal you paint the board accordingly.
				# print("Inside mouse event down, selected Piece {}",self.selected_piece)
				if self.hop == False:
					if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

						self.board.move_piece(self.selected_piece, self.mouse_pos)
					
						if self.mouse_pos not in self.board.adjacent(self.selected_piece):
							self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))
							self.end_turn()
							self.hop = False							

						else:
							self.end_turn()

				if self.hop == True:					
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
						self.board.move_piece(self.selected_piece, self.mouse_pos)
						self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))

					if self.board.legal_moves(self.mouse_pos, self.hop) == []:
							self.end_turn()

					else:
						self.selected_piece = self.mouse_pos

	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)
		self.board_string=self.board.board_piece_string(self.board.matrix)
		
	def terminate_game(self):
		"""Quits the program and ends the game."""
		pygame.quit()
		sys.exit()

	def main(self):
		""""This executes the game and controls its flow."""
		self.setup()

		while True: # main game loop
			self.event_loop()
			self.update()

	def end_turn(self):
		"""
		End the turn. Switches the current player. 
		end_turn() also checks for and game and resets a lot of class attributes.
		"""
		if self.turn == BLUE:
			self.turn = RED
		else:
			self.turn = BLUE

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == BLUE:
				self.graphics.draw_message("RED WINS!")
			else:
				self.graphics.draw_message("BLUE WINS!")

	def check_for_endgame(self):
		"""
		Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
		"""
		for x in range(8):
			for y in range(8):
				if self.board.location((x,y)).color == BLACK and self.board.location((x,y)).occupant != None and self.board.location((x,y)).occupant.color == self.turn:
					if self.board.legal_moves((x,y)) != []:
						return False

		return True

class Graphics:
	def __init__(self):
		self.caption = "Checkers"

		self.fps = 60
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('resources/board.png')

		self.square_size = self.window_size >> 3
		self.piece_size = self.square_size >> 1

		self.message = False

	def setup_window(self):
		"""
		This initializes the window and sets the caption at the top.
		"""
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self, board, legal_moves, selected_piece):
		"""
		This updates the current display.
		"""
		self.screen.blit(self.background, (0,0))
		
		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		"""
		Takes a board object and draws all of its squares to the display
		"""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
	def draw_board_pieces(self, board):
		"""
		Takes a board object and draws all of its pieces to the display
		"""
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size) 

					if board.location((x,y)).occupant.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x,y)), int (self.piece_size / 1.7), self.piece_size >> 2)


	def pixel_coords(self, board_coords):
		"""
		Takes in a tuple of board coordinates (x,y) 
		and returns the pixel coordinates of the center of the square at that location.
		"""
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	def board_coords(self, pixel):
		"""
		Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
		"""
		return (pixel[0] // self.square_size, pixel[1] // self.square_size)

	def highlight_squares(self, squares, origin):
		"""
		Squares is a list of board coordinates. 
		highlight_squares highlights them.
		"""
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def draw_message(self, message):
		"""
		Draws message to the screen. 
		"""
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)

class Board:
	def __init__(self,board=None):
		if board is None:
			self.matrix = self.new_board()
		else:
			matrix = [["None" for i in range(8)] for i in range(8)] 
			for x in range(8):
				for y in range(8):
					if (x % 2 != 0) and (y % 2 == 0):
						matrix[y][x] = Square(WHITE)
					elif (x % 2 != 0) and (y % 2 != 0):
						matrix[y][x] = Square(BLACK)
					elif (x % 2 == 0) and (y % 2 != 0):
						matrix[y][x] = Square(WHITE)
					elif (x % 2 == 0) and (y % 2 == 0): 
						matrix[y][x] = Square(BLACK)
			
			for x in range(8):
				for y in range(8):
					if board[x][y] == "B":
						matrix[x][y].occupant = Piece(BLUE)
					elif board[x][y] == "BK":
						matrix[x][y].occupant = Piece(BLUE)
						matrix[x][y].occupant.king=True
					elif board[x][y] == "R":			
						matrix[x][y].occupant = Piece(RED)
					elif board[x][y] == "RK":			
						matrix[x][y].occupant = Piece(RED)
						matrix[x][y].occupant.king=True
			self.matrix=matrix
		
	def new_board(self):
		"""
		Create a new board matrix.
		"""

		# initialize squares and place them in matrix

		matrix = [["None" for i in range(8)] for i in range(8)] 

		# The following code block has been adapted from
		# http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		# initialize the pieces and put them in the appropriate squares

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(RED)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLUE)

		return matrix

	def board_piece_string(self,board):
		"""
		Returns the current board state as a numpy array
		"""	
		board_string = [["None" for i in range(8)] for i in range(8)] 
		
		for x in range(8):
			for y in range(8):
				if board[x][y].occupant == None:
					board_string[x][y] = "N"
					continue
				if board[x][y].occupant.color == BLUE:					
					if  board[x][y].occupant.king:
						board_string[x][y] = "BK"
					else:
						board_string[x][y] = "B"						
				elif board[x][y].occupant.color == RED:
					if  board[x][y].occupant.king:
						board_string[x][y] = "RK"
					else:
						board_string[x][y] = "R"
		return np.array(board_string)
	
	'''
	Need to create an equivalent version which also includes pieces on the board
	'''
	def board_string(self, board):
		"""
		Takes a board and returns a matrix of the board space colors. Used for testing new_board()
		"""

		board_string = [["None" for i in range(8)] for i in range(8)] 

		for x in range(8):
			for y in range(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string
	
	def rel(self, dir, pixel):
		"""
		Returns the coordinates one square in a different direction to (x,y).

		===DOCTESTS===

		>>> board = Board()

		>>> board.rel(NORTHWEST, (1,2))
		(0,1)

		>>> board.rel(SOUTHEAST, (3,4))
		(4,5)

		>>> board.rel(NORTHEAST, (3,6))
		(4,5)

		>>> board.rel(SOUTHWEST, (2,5))
		(1,6)
		"""
		x = pixel[0]
		y = pixel[1]
		if dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0

	def adjacent(self, pixel):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""
		x = pixel[0]
		y = pixel[1]

		return [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)),self.rel(SOUTHWEST, (x,y)),self.rel(SOUTHEAST, (x,y))]

	def location(self, pixel):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""
		x = pixel[0]
		y = pixel[1]

		return self.matrix[x][y]

	def blind_legal_moves(self, pixel):
		"""
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board. 
		If that location is empty, then blind_legal_moves() return an empty list.
		"""

		x = pixel[0]
		y = pixel[1]
		if self.matrix[x][y].occupant != None:
			
			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y))]
				
			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
				blind_legal_moves = [self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)), self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def legal_moves(self, pixel, hop = False,board=None):
		"""
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""
		# print("Getting legal for {}".format(pixel),board)
		x = pixel[0]
		y = pixel[1]
		blind_legal_moves = self.blind_legal_moves((x,y)) 
		# print(blind_legal_moves)
		legal_moves = []
		# print("These are the blind legal moves",blind_legal_moves,x,y)
		if board is not None:
			for move in blind_legal_moves:
				if board.on_board(move):
					if board.location(move).occupant == None:
						legal_moves.append(move)

					elif board.location(move).occupant.color != board.location((x,y)).occupant.color and board.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and board.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		else:
			if hop == False:
				for move in blind_legal_moves:
					if hop == False:
						if self.on_board(move):
							if self.location(move).occupant == None:
								legal_moves.append(move)

							elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
								legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
			else: # hop == True
				for move in blind_legal_moves:
					if self.on_board(move) and self.location(move).occupant != None:
						if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves

	def remove_piece(self, pixel):
		"""
		Removes a piece from the board at position (x,y). 
		"""
		x = pixel[0]
		y = pixel[1]
		self.matrix[x][y].occupant = None

	def move_piece(self, pixel_start, pixel_end):
		"""
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""
		start_x = pixel_start[0]
		start_y = pixel_start[1]
		end_x = pixel_end[0]
		end_y = pixel_end[1]

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))

		self.king((end_x, end_y))

	def is_end_square(self, coords):
		"""
		Is passed a coordinate tuple (x,y), and returns true or 
		false depending on if that square on the board is an end square.

		===DOCTESTS===

		>>> board = Board()

		>>> board.is_end_square((2,7))
		True

		>>> board.is_end_square((5,0))
		True

		>>>board.is_end_square((0,5))
		False
		"""

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	def on_board(self, pixel):
		"""
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false.

		===DOCTESTS===
		>>> board = Board()

		>>> board.on_board((5,0)):
		True

		>>> board.on_board(-2, 0):
		False

		>>> board.on_board(3, 9):
		False
		"""

		x = pixel[0]
		y = pixel[1]
		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, pixel):
		"""
		Takes in (x,y), the coordinates of square to be considered for kinging.
		If it meets the criteria, then king() kings the piece in that square and kings it.
		"""
		x = pixel[0]
		y = pixel[1]
		if self.location((x,y)).occupant != None:
			if (self.location((x,y)).occupant.color == BLUE and y == 0) or (self.location((x,y)).occupant.color == RED and y == 7):
				self.location((x,y)).occupant.king = True 

class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object

def main():
	game = Game()
	game.main()

if __name__ == "__main__":
	main()