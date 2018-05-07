import pygame
import sys
from pygame.locals import *
from constants import *
from classes import *

# refresh the GUI
def updateGUI(board):
	# load the background image
	screen.blit(pygame.image.load('checkers_background.png'), (0, 0))
	highlightTiles(board)
	initPieces(board)
	# if there is a message, show it 
	if board.hasDisplayMessage:
		screen.blit(board.textSurfaceObj, board.textRectObj)
	pygame.display.update()
	clock.tick(40)

# draw the pieces
def initPieces(board):
	for x in range(BOARDSIZE):
		for y in range(BOARDSIZE):
			if board.boardState[x][y].contains != None:
				pygame.draw.circle(screen,board.boardState[x][y].contains.color,getPixelCoordinates((x,y)),PIECESIZE) 
				pygame.draw.circle(screen,RED,getPixelCoordinates((x,y)),PIECESIZE,4) 

# gets the coordinates of the pixel
def getPixelCoordinates(getBoardCoordinates):
	return (getBoardCoordinates[1] * TILESIZE + PIECESIZE, getBoardCoordinates[0] * TILESIZE + PIECESIZE)

# return the x,y coordinates of a piece
def getBoardCoordinates((x, y)):
	return (y/TILESIZE, x/TILESIZE)	

# highlights the possible moves
def highlightTiles(board):
	for coord in board.selectedPieceMoves:
		pygame.draw.rect(screen,YELLOW,(coord[1][1] * TILESIZE,coord[1][0] * TILESIZE,TILESIZE,TILESIZE))	
	if len(board.selectedPieceMoves) > 0 and board.selectedPieceMoves[0][0] == board.selectedPiece:
		pygame.draw.rect(screen,RED,(board.selectedPiece[1] * TILESIZE,board.selectedPiece[0] * TILESIZE,TILESIZE,TILESIZE))
		
# put message in middle of GUI
def drawMessage(board,message):
	board.hasDisplayMessage = True
	message = " " + message + " "
	board.textSurfaceObj = fontObj.render(message,True,BLUE,WHITE)
	board.textRectObj = board.textSurfaceObj.get_rect()
	board.textRectObj.center = (300,300)
