from constants import *

class Board(object):
	def __init__(self):
		self.boardState = self.getNewBoard()
    # default depth to beginner
		self.level = LEVEL1
		self.turn = None
		self.selectedPiece = None
		self.selectedPieceMoves = []
		self.allPossibleMoves = []
		# member variables to help display messages
		self.hasDisplayMessage = False
		self.textSurfaceObj = None
		self.textRectObj = None

	# initialize the board
	def getNewBoard(self):
		boardState = [[None for x in range(BOARDSIZE)] for y in range(BOARDSIZE)]

		# loop to initialize the tile pieces
		for x in range(BOARDSIZE):
			for y in range(BOARDSIZE):
				if (x % 2 == 0) and (y % 2 == 0):
					boardState[x][y] = Tile(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					boardState[x][y] = Tile(WHITE)
				elif (x % 2 == 0) and (y % 2 != 0):
					boardState[x][y] = Tile(BLACK)
				elif (x % 2 != 0) and (y % 2 == 0):
					boardState[x][y] = Tile(BLACK)

		# loop to initialize the chess pieces
		for y in range(BOARDSIZE):
			for x in range(2):
				if boardState[x][y].color == BLACK:
			          # initialize with white pieces
					boardState[x][y].contains = Piece(WHITE)

			for x in range(4, BOARDSIZE):
				if boardState[x][y].color == BLACK:
			          # initialize with black pieces
					boardState[x][y].contains = Piece(BLACK)
		return boardState

class Piece(object):
	def __init__(self, color):
		self.color = color

class Tile(object):
	def __init__(self, color, piece=None):
		self.color = color
		# tiles contain nothing by default
		self.contains = piece
