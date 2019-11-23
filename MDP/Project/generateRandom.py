import random
from utils import numStates, dotList
from variables import NORTH, EAST, SOUTH, WEST
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output")
parser.add_argument("--seed")
args=parser.parse_args()

random.seed(int(args.seed))

movements=[NORTH, EAST, SOUTH, WEST]
N=numStates*numStates*int(2**len(dotList))

with open(args.output, 'w') as f:
	for i in range(N-1):
		f.write('%d ' %(random.choice(movements)))
	f.write('%d' %(random.choice(movements)))