import argparse
from variables import FREE, BLOCKED, PACMAN, DOT, GHOST, NORTH, EAST, SOUTH, WEST
from utils import dotList, stateMapping, stateList, grid, ROWS, COLS
from utils import getState, getLocations
from utils import numStates, numActions, pacmanStartPos, ghostStartPos

parser = argparse.ArgumentParser()
parser.add_argument("--pacmanPolicy")
parser.add_argument("--mdpfile")
args=parser.parse_args()

transitionReward=-1
endReward=-1000
eatReward=1000
dotReward=-200
discount=0.95

transitions=[]
pacmanPolicy=[]

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

def addTransition(initialState, action):
	global transitions
	global dotList
	initPacman, initGhost, initDots=getLocations(initialState)
	sumDots=sum(initDots)
	if(sumDots==0 or initPacman==initGhost): #End state
		return
	nextPacman=moveDirection(initPacman, pacmanPolicy[initialState])
	nextGhost=moveDirection(initGhost, action)
	if(nextGhost==initGhost):
		return
	if(nextPacman==nextGhost):
		reward=eatReward
	elif((nextPacman in dotList) and initDots[dotList.index(nextPacman)]==1 and sumDots==1):
		reward=endReward
	elif((nextPacman in dotList) and initDots[dotList.index(nextPacman)]==1):
		reward=dotReward
	else:
		reward=transitionReward
	if((nextPacman in dotList)):
		initDots[dotList.index(nextPacman)]=0
	finalState=getState(nextPacman, nextGhost, initDots)
	transitions.append((initialState, action, finalState, reward, 1))
	return


def parsePacman():
	global pacmanPolicy
	with open(args.pacmanPolicy, 'r') as f:
		pacmanPolicy=list(map(int, f.readlines()[0].split(' ')))

parsePacman()

totalStates=numStates*numStates*int(2**len(dotList))
for state in range(totalStates):
	for action in range(numActions):
		addTransition(state, action)

with open(args.mdpfile, 'w') as f:
	f.write("numStates %d\n" %(totalStates))
	f.write("numActions %d\n" %(numActions))
	for transition in transitions:
		f.write("transition %d %d %d %d %d\n" %transition)
	f.write("discount %f\n" %(discount))