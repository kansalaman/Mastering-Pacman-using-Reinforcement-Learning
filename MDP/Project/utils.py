#assume that the grid is in grid.txt(hardcoded)
from variables import *

#numStates=valid states in board, not combined
def getState(pacman, ghost, dots): #dots is a list of 0's and 1's
	global numStates
	state=0
	for i in range(len(dots)):
		state+=dots[i]*int(2**i)
	state+=ghost*int(2**len(dots))
	state+=pacman*int(2**len(dots))*numStates
	return state

def getLocations(finalState):
	global numStates
	global dotList
	dots=[]
	for i in range(len(dotList)):
		dots.append(finalState%2)
		finalState=finalState//2
	ghost=finalState%numStates
	pacman=finalState//numStates
	return pacman, ghost, dots

stateMapping=[]
dotList=[]
stateList=[]

with open('grid.txt','r') as f:
	rows=f.readlines()
	ROWS=len(rows)
	for i in range(ROWS):
		rows[i]=list(map(int, rows[i].split(' ')))
	numStates=0
	numActions=4
	pacmanStartPos=0
	ghostStartPos=0
	COLS=len(rows[0])
	stateMapping=[[None]*COLS for rowNo in range(ROWS)]
	for i in range(ROWS):
		for j in range(COLS):
			if(rows[i][j]==BLOCKED):
				continue
			cur=numStates
			stateList.append((i,j))
			stateMapping[i][j]=cur
			numStates+=1
			if(rows[i][j]==PACMAN):
				pacmanStartPos=stateMapping[i][j]
			if(rows[i][j]==GHOST):
				ghostStartPos=stateMapping[i][j]
			if(rows[i][j]==DOT):
				dotList.append(cur)
	grid=rows