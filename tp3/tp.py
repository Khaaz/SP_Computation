import random
import math


# 20 -> 1 min
# 100 -> 1 min
# 1000 -> 10 min
# 10000 -> 10 min

#Brute force:
'''
add nearest point over and over from the last poit
'''

# triangle:
''' 
pick 3 random point to create a triangle
find nearest point, add point
'''

# convexe:
'''
create convex hull
add nearest point (inside)
'''

# get nearest distance
'''
  C
A  B

A->C + C->B - A-B
'''

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
	top = halfch(sorted(v, key=lambda p: p.x))
	bottom = halfch(sorted(v, key=lambda p: p.x, reverse=True))
	return top[0:-1] + bottom[0:-1]

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

# Calculate full dist inthe list + last -> first dist as well
# AKA whole hull dist
def calculateFullDist(base):
	
	dist = 0
	tot = len(base)
	for x in range(tot):
		if x == tot - 1:
			# dist last -> first
			dist += base[x].dist(base[0])
		else:
			dist += base[x].dist(base[x + 1])
	
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
	neighbours = dict()
	tot = len(hull)
	for index in range(tot):
		if index == tot - 1:
			# last -> first
			createNeighbour(neighbours, hull[len(hull) - 1], hull[0], free)
		else:
			createNeighbour(neighbours, hull[index], hull[index + 1], free)
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
	

# Read stdin
nbr = int(input())

# create list of Point
base = [Point(input().split(' ')) for i in range(nbr)]
# create list of tuple
#base = [tuple(float(i) for i in input().split(' ')) for i in range(nbr)]

hull = chP(base)
#free = [ x for x in base if x not in hull ]
free = set(base) - set(hull)

neighbours = createAllNeighbours(hull, free)

# Add point until all point are in the hull
while free:
	addPoint(hull, free, neighbours)

# Print
# nbr de point
print(nbr)
# distance tot(with last -> first dist)
print(calculateFullDist(hull))
# all point in order
[print(e) for e in hull]
