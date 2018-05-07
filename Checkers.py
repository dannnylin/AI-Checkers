import time
from graphics import *
from copy import deepcopy
from constants import *
from classes import *

# show menu and home screen
def menu(board):
	global screen
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit
		screen.fill(WHITE)
		# display the checkers logo
		logo = pygame.image.load("checkers-logo.png").convert()
		# position the logo
		screen.blit(logo, (110, 125))
		button("Go First", 150, 475, 100, 50, BLUE, board, action="first")
		button("Go Second", 350, 475, 100, 50, BLUE, board, action="second")
		button("Quit", 0, 575, 600, 25, BLACK, board, action="quit")
		drawButton(board)
		pygame.display.update()

def drawButton(board):
	button("Level 1", 50, 400, 100, 50, BLACK, board, action="level1")
	button("Level 2", 250, 400, 100, 50,
	       BLACK, board, action="level2")
	button("Level 3", 450, 400, 100, 50, BLACK, board, action="level3")
	if board.level == LEVEL1:
		button("Level 1", 50, 400, 100, 50, RED, board, action="level1")
	elif board.level == LEVEL2:
		button("Level 2", 250, 400, 100, 50,
		       RED, board, action="level2")
	elif board.level == LEVEL3:
		button("Level 3", 450, 400, 100, 50, RED, board, action="level3")

def button(text, x, y, w, h, color, board, action=None):  # Create game intro buttons
	pygame.draw.rect(screen, color, (x, y, w, h))
	textSurface = fontObjSmall.render(text, True, WHITE)
	textRect = textSurface.get_rect()
	textRect.center = ((x+(w/2)), (y+(h/2)))
	screen.blit(textSurface, textRect)
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		if click[0] == 1 and action != None:
			if action == "level1":
				board.level = LEVEL1
				pass
			elif action == "level2":
				board.level = LEVEL2
				pass
			elif action == "level3":
				board.level = LEVEL3
				pass
			elif action =="quit":
				pygame.quit()
				sys.exit()
			else:
				board.turn = BLACK if action == "first" else WHITE
				print("Starting the game")
				print("You selected level")
				displayGame(board)


def displayGame(board): 
	refresh(board)  
	# loop to keep game running
	while True: 
		event_loop(board) 
		# update game interface
		updateGUI(board)  

# load alpha beta value
def refresh(board): 
	board.selectedPiece = None
	board.selectedPieceMoves = []
	# ai's turn
	if board.turn == WHITE:  
		move = alphaBetaSearch(board)
		# if no move available, skip turn
		if move != None:  
			movePiece(board, move)  
		endTurn(board)  
	# human move
	else:
		board.allPossibleMoves = getForcedCaptureMoves(board, board.turn)

# function to help determine click actions and pieces
def event_loop(board):
	mouse_pos = getBoardCoordinates(pygame.mouse.get_pos())
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit
		# on mouse left click
		if event.type == MOUSEBUTTONDOWN:
			if board.selectedPiece != None:
				if board.selectedPiece == mouse_pos:
					board.selectedPiece = None
					board.selectedPieceMoves = []
					break
				# checks to see if move is valid
				for move in board.selectedPieceMoves: 
					if move[1] == mouse_pos: 
						movePiece(board, move)  
						board.selectedPiece = None
						board.selectedPieceMoves = []
						endTurn(board) 
			board.selectedPiece = mouse_pos 
			board.selectedPieceMoves = getLegalMoves(board) 
	# if there is no move and no message to display, end the turn
	if not board.hasDisplayMessage and board.allPossibleMoves == []:
		endTurn(board)

# end the user's turn
def endTurn(board):  
	# swap 
	if board.turn == BLACK: 
		board.turn = WHITE
	else:
		board.turn = BLACK
	# load alpha beta
	refresh(board)  
	# update the GUI
	updateGUI(board) 
	if checkEndGame(board):
		blackCount = countPiecesForColor(board, BLACK)
		whiteCount = countPiecesForColor(board, WHITE)
		if blackCount == whiteCount:  # draw
			drawMessage(board, "Its a tie!")
		elif blackCount > whiteCount:  
			drawMessage(board, "You win!")
		else: 
			drawMessage(board, "AI wins!")

# Check if both player are out of moves or a player is out of pieces
def checkEndGame(board):
	# both players no longer have moves
	if ((len(getForcedCaptureMoves(board, WHITE))) + (len(getForcedCaptureMoves(board, BLACK))) == 0): 
		return True
	# checks if a player is out of pieces
	if (countPiecesForColor(board, BLACK) == 0) or (countPiecesForColor(board, WHITE) == 0):
		return True
	return False

def directionToCoordinates(direction, (x, y)):
	if direction == TOPLEFT:
		return (x-1, y-1)
	elif direction == TOPRIGHT:
		return (x-1, y+1)
	elif direction == BOTTOMLEFT:
		return (x+1, y-1)
	elif direction == BOTTOMRIGHT:
		return (x+1, y+1)
	return (0, 0)

def getAllPiecesOf(board, color):
	allColorPieces = []
	for x in range(BOARDSIZE):
		for y in range(BOARDSIZE):
			# checks to see if it is a piece and color of piece
			if getPiece(board, (x, y)) != None and getColor(board, (x, y)) == color:
				if color == BLACK:
					if(getPiece(board, (x, y)).color == BLACK):
						temp = directionToCoordinates(TOPLEFT, (x, y))
						temp2 = directionToCoordinates(TOPRIGHT, (x, y))
						if (isOnBoard(temp) and (getPiece(board, temp) == None or getPiece(board, temp).color != BLACK)) or (isOnBoard(temp2) and (getPiece(board, temp2) == None or getPiece(board, temp2).color != BLACK)):
							allColorPieces.append((x, y))
				if color == WHITE:
					if(getPiece(board, (x, y)).color == WHITE):
						temp = directionToCoordinates(BOTTOMLEFT, (x, y))
						temp2 = directionToCoordinates(BOTTOMRIGHT, (x, y))
						if (isOnBoard(temp) and (getPiece(board, temp) == None or getPiece(board, temp).color != WHITE)) or (isOnBoard(temp2) and (getPiece(board, temp2) == None or getPiece(board, temp2).color != WHITE)):
							allColorPieces.append((x, y))
	return allColorPieces

def getForcedCaptureMoves(board, color):
	allForceMoves = []
	possibleMoves = getAllPiecesOf(board, color)
	# no possible moves
	if len(possibleMoves) == 0: 
		return []
	for move in possibleMoves:
		if color == BLACK:
			temp = directionToCoordinates(TOPLEFT, move)
			if isOnBoard(temp) and getPiece(board, temp) != None and getColor(board, temp) != color:
				temp2 = directionToCoordinates(TOPLEFT, temp)
				if isOnBoard(temp2) and getPiece(board, temp2) == None:
					allForceMoves.append([move, temp2, temp])
			temp = directionToCoordinates(TOPRIGHT, move)
			if isOnBoard(temp) and getPiece(board, temp) != None and getColor(board, temp) != color:
				temp2 = directionToCoordinates(TOPRIGHT, temp)
				if isOnBoard(temp2) and getPiece(board, temp2) == None:
					allForceMoves.append([move, temp2, temp])
		else:
			temp = directionToCoordinates(BOTTOMLEFT, move)
			if isOnBoard(temp) and getPiece(board, temp) != None and getColor(board, temp) != color:
				temp2 = directionToCoordinates(BOTTOMLEFT, temp)
				if isOnBoard(temp2) and getPiece(board, temp2) == None:
					allForceMoves.append([move, temp2, temp])
			temp = directionToCoordinates(BOTTOMRIGHT, move)
			if isOnBoard(temp) and getPiece(board, temp) != None and getColor(board, temp) != color:
				temp2 = directionToCoordinates(BOTTOMRIGHT, temp)
				if isOnBoard(temp2) and getPiece(board, temp2) == None:
					allForceMoves.append([move, temp2, temp])
	if len(allForceMoves) == 0:
		return getAllLegalMoves(board, color, possibleMoves)
	return allForceMoves

def getAllLegalMoves(board, color, possibleMoves):
	allLegalMoves = []
	for move in possibleMoves:
		if color == BLACK:
			temp = directionToCoordinates(TOPLEFT, move)
			if isOnBoard(temp) and getPiece(board, temp) == None:
					allLegalMoves.append([move, temp])
			temp = directionToCoordinates(TOPRIGHT, move)
			if isOnBoard(temp) and getPiece(board, temp) == None:
					allLegalMoves.append([move, temp])
		if color == WHITE:
			temp = directionToCoordinates(BOTTOMLEFT, move)
			if isOnBoard(temp) and getPiece(board, temp) == None:
					allLegalMoves.append([move, temp])
			temp = directionToCoordinates(BOTTOMRIGHT, move)
			if isOnBoard(temp) and getPiece(board, temp) == None:
					allLegalMoves.append([move, temp])
	return allLegalMoves

def getLegalMoves(board):  # Returns list of legal moves based on selected move
	selectedPieceMoves = []
	for move in board.allPossibleMoves:
		if move[0] == board.selectedPiece:
			selectedPieceMoves.append(move)
	return selectedPieceMoves

# remove a piece after captured
def deletePiece(board, (x, y)): 
	board.boardState[x][y].contains = None

def movePiece(board, move):
	if len(move) == 3:  # remove jumped piece
		deletePiece(board, move[2])
	board.boardState[move[1][0]][move[1][1]
                                  ].contains = board.boardState[move[0][0]][move[0][1]].contains  # move piece
	deletePiece(board, (move[0][0], move[0][1]))  # remove old piece

# determine if coordinate is on the board (within bounds)
def isOnBoard((x, y)): 
	return (x >= 0 and x < BOARDSIZE) and (y >= 0 and y < BOARDSIZE)

# get piece at board tile coordinates if there is one
def getPiece(board, (x, y)): 
	return board.boardState[x][y].contains

# gets the color of a piece
def getColor(board, (x, y)): 
	return board.boardState[x][y].contains.color

# return number of pieces left for a color
def countPiecesForColor(board, color):
	count = 0
	for x in range(BOARDSIZE):
		for y in range(BOARDSIZE):
			if board.boardState[y][x].contains != None and board.boardState[y][x].contains.color == color:
				count += 1
	return count

def canCapture(board, currentturn):  # counts jump moves for a player
	moves = getForcedCaptureMoves(board, currentturn)
	if len(moves) > 0 and len(moves[0]) == 3:
		if currentturn == BLACK:
			# human can capture
			return -len(moves) 
			# ai can capture
		return len(moves)  
	return 0

# checks if piece is safe, there are two friendly pieces preventing a jump
def isSafe(board, (x, y), color):
	if color == BLACK:
		temp = directionToCoordinates(BOTTOMLEFT, (x, y))
		temp2 = directionToCoordinates(BOTTOMRIGHT, (x, y))
	else:
		temp = directionToCoordinates(TOPLEFT, (x, y))
		temp2 = directionToCoordinates(TOPRIGHT, (x, y))
	if ((not isOnBoard(temp)) or (getPiece(board, temp) != None and getPiece(board, temp).color == color)) and ((not isOnBoard(temp2)) or (getPiece(board, temp2) != None and getPiece(board, temp2).color == color)):
		return True
	return False

def alphaBetaSearch(boardState):  # alpha beta search
	global depthOfTree, totalNodesGenerated, maximumPruning,  minimumPruning, totalTimeElapsed, cutOff
	depthOfTree = 0
	totalNodesGenerated = 0
	maximumPruning = 0
	minimumPruning = 0
	# end time used to calculate time elapsed
	totalTimeElapsed = time.time()
	cutOff = False
	chosenMove = maxValue(boardState, -1000, 1000, 0)
	print "Total Number of Nodes Generated: %s " % totalNodesGenerated
	print "Times Pruning Occurred in Maximum Value: %s " % maximumPruning
	print "Times Pruning Occurred in Minimum Value: %s " % minimumPruning
	print "Total Time Elapsed: %f " % (time.time() - totalTimeElapsed)
	if cutOff:
		print "Cut-off Depth: %s " % boardState.level
	else:
		print "Maximum Depth of Tree: %s " % depthOfTree
	# the search returns a tuple in which the 2nd element is the best move
	return chosenMove[1]

def maxValue(boardState, alpha, beta, depth):
	global depthOfTree, totalNodesGenerated, maximumPruning
	depthOfTree = max(depth, depthOfTree)
	totalNodesGenerated += 1
	# check to see if game is over
	if checkEndGame(boardState): 
		blackCount = countPiecesForColor(boardState, BLACK)
		whiteCount = countPiecesForColor(boardState, WHITE)
		# game is tied at this point
		if blackCount == whiteCount:
			return (0, None) 
		elif blackCount > whiteCount:
			# human wins
			return (-1000, None)
		else:
			# ai wins
			return (1000, None)
	if shouldCutOff(boardState):
		return evaluation(boardState, WHITE)
	v = -1000
	# get all valid ai moves
	actions = getForcedCaptureMoves(boardState, WHITE)
	bestMove = None
	for action in actions:
		# make a copy of the current board
		tempBoard = deepcopy(boardState) 
		# move the piece and get the utility vlaue
		movePiece(tempBoard, action)  
		chosenMinValue = minValue(tempBoard, alpha, beta, depth+1)[0]
		if v <= chosenMinValue: 
			v = chosenMinValue
			bestMove = action
		if v >= beta:
			maximumPruning += 1
			return (v, action)
		alpha = max(alpha, v)
	return (v, bestMove)

def minValue(boardState, alpha, beta, depth):
	global depthOfTree, totalNodesGenerated, minimumPruning
	depthOfTree = max(depth, depthOfTree)
	totalNodesGenerated += 1
	# check to see if game is over
	if checkEndGame(boardState): 
		blackCount = countPiecesForColor(boardState, BLACK)
		whiteCount = countPiecesForColor(boardState, WHITE)
		# game is tied at this point
		if blackCount == whiteCount:
			return (0, None)
		elif blackCount > whiteCount:
			# human wins
			return (-1000, None) 
		else:
			# ai wins
			return (1000, None)
	if shouldCutOff(boardState):
		return evaluation(boardState, BLACK)
	v = 1000
	actions = getForcedCaptureMoves(boardState, BLACK)
	bestMove = None
	for action in actions:
		# make a copy of the current board
		tempBoard = deepcopy(boardState)  
		# move the piece and get the utility vlaue
		movePiece(tempBoard, action) 
		chosenMaxValue = maxValue(tempBoard, alpha, beta, depth+1)[0]
		if v >= chosenMaxValue: 
			v = chosenMaxValue
			bestMove = action
		if v <= alpha:
			minimumPruning += 1
			return (v, action)
		beta = min(beta, v)
	return (v, bestMove)

def shouldCutOff(boardState):
	global depthOfTree
	cutOff = True
	# cut off if depth is greater than set difficulty level
	return depthOfTree >= boardState.level  

def getEndPieceCount(board):
	result = [0,0]
	for y in range(BOARDSIZE):
		if board.boardState[0][y].contains != None:
			if board.boardState[0][y].contains.color == BLACK:
				result[1] += 1
		if board.boardState[5][y].contains != None:
			if board.boardState[5][y].contains.color == WHITE:
				result[0] += 1
	return result

def getProtectedPieceCount(board, color):
	count = 0
	for x in range(BOARDSIZE):
		for y in range(BOARDSIZE):
			# if it is a piece
			if getPiece(board, (x,y)) != None:
				# could get color if it is a piece
				if getColor(board, (x,y)) == color:
					# if it is safe, add 1 to the count
					if isSafe(board, (x,y), color):
						count += 1
					# if it is on the edge which means it can't be captured, add 1 to the count
					if y is 0 or y is 5:
						count += 1
	return count

def evaluation(board, color):
	value = 0
	whiteCountValue = 100 * countPiecesForColor(board, WHITE)
	blackCountValue = -100 * countPiecesForColor(board, BLACK)
	value += (whiteCountValue - blackCountValue)
	whiteCaptureCountValue =  canCapture(board, WHITE) * 250
	blackCaptureCountValue = canCapture(board, BLACK) * -250
	value += (whiteCaptureCountValue - blackCaptureCountValue)
	endPieceScore = getEndPieceCount(board)
	whiteEndPieceScore, blackEndPieceScore = endPieceScore[0] * 200, endPieceScore[1] * -200
	value += (whiteEndPieceScore - blackEndPieceScore)
	whiteProtectedScore = getProtectedPieceCount(board, WHITE) * 150
	blackProtectedScore = getProtectedPieceCount(board, BLACK) * -150
	value += (whiteProtectedScore - blackProtectedScore)
	return (value, None)

board = Board()
# init game
pygame.init()
# set window title
pygame.display.set_caption("Checkers - AI Project")
menu(board)
