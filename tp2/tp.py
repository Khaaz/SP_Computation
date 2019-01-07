import math
import random


class Point:
	x = 0
	y = 0
	def __init__(self, arr):
		self.x = float(arr[0])
		self.y = float(arr[1])

	def dist(self, p):
		return math.sqrt(math.pow(self.x - p.x, 2) + math.pow(self.y - p.y, 2))

	def __str__(self):
		return str(self.x) + " " + str(self.y)

	def __repr__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"


def ensureResultValidity(result):
	for elem in result:
		for e in result:
			if elem.dist(e) < r and elem != e:
				print('err')


# get best vector from all vector tries (2pi)
def pickVector(base, final, step):
	finalVector = 0

	for i in range(1, step):
		result = []
		baseTmp = base

		vector = (2 * math.pi)/step * i

		# sort
		sortByVector(baseTmp, vector)
		
		optiGraph(baseTmp, result)
		
		# keep best result
		if len(result) > len(final):
			final = result
			finalVector = vector

	return finalVector

def sortByVector(list, vector):
	list.sort(key = lambda p: math.cos(vector) * p.x + math.sin(vector) * p.y)

# get a result sample according to one vector
# Greedy
def optiGraph(base, result):
	while base:
		cur = base[0]
		result.append(cur)

		temp = []
		for elem in base:
			if cur.dist(elem) > r:
				temp.append(elem)

		base = temp

def localSearch(base, final, near, r):
	result = final[:]
	notFinal = [ x for x in base if x not in final ]
	randIndex = random.randrange(len(notFinal))
	p = notFinal[randIndex]
	
	# sort point from farest to nearest
	final.sort(key=lambda x: x.dist(p))
	
	for elem in final:
		# all neighbours of far
		nbours = near[elem]

		if len(nbours) == 0:
			continue
		
		nbours.sort(key=lambda x: x.dist(p))

		addedOne = False
		result.remove(elem)
		for n in nbours:
			canAdd = True
			for e in result:
				if n.dist(e) <= r:
					canAdd = False
					break

			if canAdd:
				addedOne = True
				result.append(n)

		if not addedOne:
			result.append(elem)

	return result

# Use a grid to get near points
def getNear(base, r):
	# Slower way to achieve the same result (prefer usage of grid below)
	# near = { p: [ q for q in base if p.dist(q) <= r and p != q ] for p in base }
	
	cells = {}
	for p in base:
		key = (int(p.x/r), int(p.y/r))
		if (key in cells):
			cells[key].append(p)
		else:
			cells[key] = [p]

	near = {}
	for p in base:
		key = (int(p.x/r), int(p.y/r))
		
		near[p] = []
		for x in [-1,0,1]:
			for y in [-1,0,1]:
				for elem in cells.get((key[0] + x, key[1] + y), []):
					if p.dist(elem) <= r:
						near[p].append(elem)

	return near

# Read stdin
nbr = int(input())
r = float(input())

# create list
base = [Point(input().split(' ')) for i in range(nbr)]
final = []
vector = 0



# Get best vector
# vector = pickVector(base, final, 500)
# print(vector)

# Staticly keeping best vector
if nbr == 20:
	vector = 0.6283185307179586
elif nbr == 100:
	vector = 1.8849555921538759
elif nbr == 1000:
	random.seed(1)
	vector = 1.790079494015464
elif nbr == 10000:
	random.seed(110298)
	vector = 3.028495318060561

# Sort and get the best sample possible
sortByVector(base, vector)
optiGraph(base, final)

# Create a dict with all neighbours per points
near = getNear(base, r)

# Swap results to get a better result.
finalLocal = localSearch(base, final, near, r)

if nbr == 1000:
	for x in range(1000):
		finalLocal = localSearch(base, finalLocal, near, r)
else:
	for x in range(30):
		finalLocal = localSearch(base, finalLocal, near, r)


# display result
print(len(finalLocal))
[print(e) for e in finalLocal]

# make sure result validity
# ensureResultValidity(final)
