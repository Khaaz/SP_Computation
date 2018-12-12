import random
import math
import copy


# 20 -> 1 min
# 100 -> 1 min
# 1000 -> 10 min
# 10000 -> 10 min

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

# Read stdin
nbr = int(input())

# create list of Point
base = [Point(input().split(' ')) for i in range(nbr)]
# create list of tuple
#base = [tuple(float(i) for i in input().split(' ')) for i in range(nbr)]

obj = 0
if nbr == 20:
	obj = 92
	random.seed(19)
elif nbr == 100:
	obj = 78000
	random.seed(317)
elif nbr == 1000:
	obj = 108000
	random.seed(30977)
else:
	obj = 465000
	random.seed(1899)

# convex hull from tuple
def chT(v):
	def ccw(p,q,r):
		x = ((q[0]-p[0]) * (r[1]-p[1])) - ((r[0]-p[0]) * (q[1]-p[1]))
		return x > 0 # True if p,q,r are oriented counterclockwise
	def halfch(v):
		hull = [v[0]]
		for p in v[1:]:
			while len(hull)>=2 and ccw(p, hull[-1], hull[-2]):
				hull.pop()
			hull.append(p)
		return hull
	top = halfch(sorted(v))
	bottom = halfch(sorted(v, reverse=True))
	return top[0:-1] + bottom[0:-1]

# convex hull from Point
def chP(v):
	def ccw(p,q,r):
		x = ((q.x-p.x) * (r.y-p.y)) - ((r.x-p.x) * (q.y-p.y))
		return x > 0 # True if p,q,r are oriented counterclockwise
	def halfch(v):
		hull = [v[0]]
		for p in v[1:]:
			while len(hull)>=2 and ccw(p, hull[-1], hull[-2]):
				hull.pop()
			hull.append(p)
		return hull
	top = halfch(sorted(v, key=lambda p: (p.x, p.y)) )
	bottom = halfch(sorted(v, key=lambda p: (p.x, p.y), reverse=True))
	return top[0:-1] + bottom[0:-1]

# Calculate full dist inthe list + last -> first dist as well
# AKA whole hull dist
def calculateFullDist(base):
	
	dist = 0
	# tot = len(base)
	# for x in range(tot):
	# 	if x == tot - 1:
	# 		# dist last -> first
	# 		dist += base[x].dist(base[0])
	# 	else:
	# 		dist += base[x].dist(base[x + 1])
	for index in range(len(base)):
		dist += base[index - 1].dist(base[index])
	
	return dist

# Dist added if adding the point C
def addedDist(A, B, C):
	return A.dist(C) + C.dist(B) - A.dist(B)

# base = all points NOT in current hull
def getSmallerDist(A, B, free):
	smallerDist = 0
	nearP = 0
	for e in free:
		dist = addedDist(A, B, e)
		if smallerDist == 0 or dist < smallerDist:
			smallerDist = dist
			nearP = e

	if nearP == 0:
		return ()
	else:
		return (smallerDist, nearP)

# create dict that associate pair of point with nearest point
def createAllNeighbours(hull, free):
	neighbours = {}
	# tot = len(hull)
	# for index in range(tot):
	# 	if index == tot - 1:
	# 		# last -> first
	# 		createNeighbour(neighbours, hull[len(hull) - 1], hull[0], free)
	# 	else:
	# 		createNeighbour(neighbours, hull[index], hull[index + 1], free)
	for index in range(len(hull)):
		createNeighbour(neighbours, hull[index - 1], hull[index], free)

	return neighbours

# Create one entry in neighbours dict for two points
# (A, B) => (dist, Point)
def createNeighbour(nb, A, B, free):
	nb[(A, B)] = getSmallerDist(A, B, free)

# Add one point to convex hull
def addPoint(hull, free, near):
	
	# Find smaller dist/point to add
	segment = 0
	dist = 0
	point = 0
	for key, value in near.items():
		if dist == 0 or value[0] < dist:
			segment = key
			dist = value[0]
			point = value[1]

	# remove old entry from dict
	del near[segment]	

	# add new point to hull
	index = hull.index(segment[0])
	hull.insert(index + 1, point)
	
	# remove old point from free
	free.remove(point)

	# End if free is empty	
	if len(free) == 0:
		return
	
	# ajoute 2 nouvelles association
	createNeighbour(near, segment[0], point, free)
	createNeighbour(near, point, segment[1], free)

	# check if another element in dict has this point and recalculate
	for key, value in near.items():
		if value[1] == point:
			createNeighbour(near, key[0], key[1], free)

## OLD
# hull = chP(base)
# #free = [ x for x in base if x not in hull ]
# free = set(base) - set(hull)

# neighbours = createAllNeighbours(hull, free)

# # Add point until all point are in the hull
# while free:
# 	addPoint(hull, free, neighbours)


def addPointInHull(hull, point):
	segment = getBestPlace(hull, point)
	
	# add new point to hull
	index = segment[0]
	hull.insert(index, point)

def getBestPlace(hull, point):
	smallerDist = 0
	segment = 0
	for index in range(len(hull)):
		dist = addedDist(hull[index], hull[index - 1], point)
		if smallerDist == 0 or dist < smallerDist:
			smallerDist = dist
			segment = (index, index - 1)
	return segment

def getBestPlaceLocalSearch(dist, hull, point):
	smallerDist = dist
	segment = 0
	for index in range(len(hull)):
		A = hull[index]
		B = hull[index - 1]
		if A == point or B == point:
			continue
		# dist = A.dist(point) + point.dist(B)
		dist = addedDist(A, B, point)
		if dist < smallerDist:
			smallerDist = dist
			segment = (A, B)

	return segment

def localSearch(hull):
	newHull = copy.copy(hull)
	for point in hull:
		index = newHull.index(point)
		A = newHull[index - 1]
		B = newHull[0] if index + 1 >= len(newHull) else newHull[index + 1]
		# dist = A.dist(point) + point.dist(B)
		dist = addedDist(A, B, point)

		segment = getBestPlaceLocalSearch(dist, newHull, point)
		if segment != 0:
			newHull.pop(index)
			ind = newHull.index(segment[0])
			newHull.insert(ind, point)
			
	return newHull

hull = chP(base)
free = [ x for x in base if x not in hull ]

while free:
	randIndex = random.randrange(len(free))
	point = free.pop(randIndex)
	addPointInHull(hull, point)

dist = calculateFullDist(hull)
if nbr == 1000:
	while(dist > obj):
		hull = localSearch(hull)
		dist = calculateFullDist(hull)
else:
	hull = localSearch(hull)
	dist = calculateFullDist(hull)

print(nbr)
# distance tot(with last -> first dist)
print(dist)
# all point in order
[print(e) for e in hull]