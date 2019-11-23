import argparse
from utils import pacmanStartPos, ghostStartPos, dotList, getLocations, stateList, getState, stateMapping
from variables import NORTH, EAST, SOUTH, WEST

#initialState is the position of pacman/ghost. Not the game state
def moveDirection(initialState, direction):
	global stateList
	initialPos=stateList[initialState]
	if(direction==NORTH):
		finalPos=(initialPos[0]-1, initialPos[1])
	elif(direction==EAST):
		finalPos=(initialPos[0], initialPos[1]+1)
	elif(direction==SOUTH):
		finalPos=(initialPos[0]+1, initialPos[1])
	elif(direction==WEST):
		finalPos=(initialPos[0], initialPos[1]-1)
	if(stateMapping[finalPos[0]][finalPos[1]]==None):
		return initialState
	else:
		return stateMapping[finalPos[0]][finalPos[1]]

# parser = argparse.ArgumentParser()
# parser.add_argument("--pacmanPolicy")
# parser.add_argument("--ghostPolicy")
# args=parser.parse_args()


pacmanPolicy=[]
def parsePacman():
	global pacmanPolicy
	with open("pacmanPolicy.txt", 'r') as f:
		pacmanPolicy=list(map(int, f.readlines()[0].split(' ')))

parsePacman()

ghostPolicy=[]
def parseGhost():
	global ghostPolicy
	with open("ghostPolicy.txt", 'r') as f:
		ghostPolicy=list(map(int, f.readlines()[0].split(' ')))

parseGhost()

currentState=getState(pacmanStartPos, ghostStartPos, [1 for i in range(len(dotList))])

def getPacmanPos():
	global currentState
	pacman, ghost, dots=getLocations(currentState)
	return stateList[pacman]

def getGhostPos():
	global currentState
	pacman, ghost, dots=getLocations(currentState)
	return stateList[ghost]

def getDotsPos():
	global currentState
	pacman, ghost, dots=getLocations(currentState)
	curDots=[]
	for i in range(len(dots)):
		if(dots[i]==1):
			curDots.append(stateList[dotList[i]])
	return curDots

def nextIteration():
	global currentState
	initPacman, initGhost, initDots=getLocations(currentState)
	nextGhost=moveDirection(initGhost, ghostPolicy[currentState])
	nextPacman=moveDirection(initPacman, pacmanPolicy[currentState])
	print(initPacman, nextPacman, initGhost, nextGhost)
	print("pacman policy", pacmanPolicy[currentState])
	print("curstate", currentState)
	
	sumDots=sum(initDots)
	if(sumDots==0 or initPacman==initGhost): #End state
		return -1 #i.e. Game must end here
	if((nextPacman in dotList)):
		initDots[dotList.index(nextPacman)]=0
	finalState=getState(nextPacman, nextGhost, initDots)
	currentState=finalState
	return 0 #All OK

# i=0
# while(i<100):
# 	i+=1
# 	# print(getPacmanPos())
# 	print(getGhostPos())
# 	if(nextIteration()==-1):
# 		break