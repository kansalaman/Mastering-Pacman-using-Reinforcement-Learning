import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mdpfile")
parser.add_argument("--output")
args=parser.parse_args()

with open(args.mdpfile,'r') as f:
	lines=f.readlines()
	for i in range(2):
		lines[i]=list(map(int, lines[i].split(' ')[1:]))
	numStates=lines[0][0]
	numActions=lines[1][0]
	# print(lines[-1].split(' '))
	discount=float(lines[-1].split(' ')[-1])
	probabilities=np.zeros((numStates, numActions, numStates))
	rewards=np.zeros((numStates, numActions, numStates))
	for i in range(2, len(lines)-1):
		current=lines[i].split(' ')[1:]
		probabilities[int(current[0]), int(current[1]), int(current[2])]=float(current[4])
		rewards[int(current[0]), int(current[1]), int(current[2])]=int(current[3])

value=np.zeros((numStates))
policy=np.zeros((numStates))
maxIterations=5
eps=1e-3

print(numStates, np.sum(probabilities), np.sum(rewards))

for i in range(maxIterations):
	actionMatrix=np.sum(probabilities*(rewards+discount*np.tile(value,(numStates, numActions, 1))), axis=2)
	actionMatrix[actionMatrix == 0] = -100000
	policy=np.argmax(actionMatrix, axis=1)
	newValue=np.ndarray.max(actionMatrix, axis=1)
	if(np.linalg.norm(newValue-value)<eps):
		break
	value=newValue
	print(np.sum(value))
	import sys
	np.set_printoptions(threshold=sys.maxsize)
	print(value)

with open(args.output,'w') as f:
	for i in range(numStates-1):

		f.write("%d "%(policy[i]))
	f.write("%d"%(policy[numStates-1]))
