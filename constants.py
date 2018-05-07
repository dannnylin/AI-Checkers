import time
import pygame
import sys
from pygame.locals import *
from enum import Enum

# color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BOARDSIZE = 6

# pygame tools
clock = pygame.time.Clock()
pygame.font.init()
fontObj = pygame.font.SysFont('Roboto', 70)
fontObjMed = pygame.font.SysFont('Roboto', 50)
fontObjSmall = pygame.font.SysFont('Roboto', 20)

global screen
screen = pygame.display.set_mode((600, 600))
TILESIZE = 600/BOARDSIZE
PIECESIZE = TILESIZE/2

# directions for tile movements
TOPLEFT = "topleft"
TOPRIGHT = "topright"
BOTTOMLEFT = "bottomleft"
BOTTOMRIGHT = "bottomright"

# difficulty according to cut-off depth
LEVEL1 = 5
LEVEL2 = 10
LEVEL3 = 20

totalNodesGenerated = 0
maximumPruning = 0
minimumPruning = 0
totalTimeElapsed = time.time()
cutOff = False
