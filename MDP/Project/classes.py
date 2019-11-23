import pygame
from pygame.locals import * 
from random import randint
import numpy as np
import simulate 
class Maze():

    def __init__(self):
	self.BLACK = (0,0,0)
	self.GOLD = (246,253,49)
	self.GREY = (50,50,50)
	self.RED = (255,0,0)
	self.BLUE = (20,27,229)
	self.WHITE = (255,255,255)	
	self.GREEN = (0,255,0)	
	self.width  = 20
	self.height = 20
	self.margin = 1	
	self.score = 0
	self.level = 1	
	self.grid = []
	# self.walls = []
	self.countfinal = 0
	self.make()
	self.size = [1000, 700]
	self.screen = pygame.display.set_mode(self.size)
	self.points = []
	

    def make(self):	
	# for i in range(2,4):
	#     for j in range(5,14):
	# 	self.walls.append([i,j])
	    input_file = open("grid.txt", 'r')
	    self.grid = np.loadtxt(input_file, dtype=int)
	
	    return self

    def reset(self):
	self.grid = []
	# self.walls = []
	self.countfinal = 0
	self.make()	
	return self


    def dispmaze(self):
	n, m  = self.grid.shape
	for row in range(n):
            for column in range(m):
                color = self.GREY
		pygame.draw.rect(self.screen,color,[(self.margin+self.width)*column+self.margin,(self.margin+self.height)*row+self.margin,self.width,self.height])
                # color = self.GOLD
	        if self.grid[row][column] == 1:
		    pygame.draw.rect(self.screen,self.BLUE,[(self.margin+self.width)*column+self.margin,(self.margin+self.height)*row+self.margin,self.width,self.height])

    def scoredisp(self):
        self.points = simulate.getDotsPos()

    def drawwalls(self):
	for wall in self.points:
            pygame.draw.rect(self.screen,self.GOLD,[(self.margin+self.width)*int(wall[1])+self.margin+7,(self.margin+self.height)*int(wall[0])+self.margin+7,self.width - 14,self.height - 14])

class Person(Maze):

	def __init__(self,x,y):
	    self.x = x	
	    self.y = y
	

class Pacman(Person):

	def __init__(self):
	    x = randint(0,6)
	    y = randint(0,4)
	    Person.__init__(self,x,y)
	
	
	def pos(self,G):
	    pygame.draw.rect(G.screen,G.GREEN,[(G.margin+G.width)*self.y+G.margin,(G.margin+G.height)*self.x+G.margin,G.width,G.height])


	def pacPosition(self,G):
	    a = simulate.getPacmanPos() 
	    print(a)
	    self.x, self.y = int(a[0]), int(a[1])
	    


class Ghost(Person):

	def __init__(self):
	    x = randint(0,6)
	    y = randint(0,6)
	    Person.__init__(self,x,y)
	

	def pos(self,G):
	    pygame.draw.rect(G.screen,G.RED,[(G.margin+G.width)*self.y+G.margin,(G.margin+G.height)*self.x+G.margin,G.width,G.height])
 
	def ghostPosition(self,G):
	    a = simulate.getGhostPos()
	    self.x , self.y = a[0], a[1]	