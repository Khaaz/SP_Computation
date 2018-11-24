import math


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
def optiGraph(base, result):
	while base:
		cur = base[0]
		result.append(cur)

		temp = []
		for elem in base:
			if cur.dist(elem) > r:
				temp.append(elem)

		base = temp

def localSearch(base, result, r):
	1 + 1

def getNear(base, r):
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
		cell = cells[key]
		
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

# Get final
vector = pickVector(base, final, 10)

sortByVector(base, vector)
optiGraph(base, final)

print(vector)

#localSearch(base, final, r)
near = getNear(base, r)
print(near)

# display result
print(len(final))
#[print(e) for e in result]

# make sure result validity
ensureResultValidity(final)
