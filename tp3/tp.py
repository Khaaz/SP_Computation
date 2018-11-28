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
	mark = False
	def __init__(self, arr):
		self.x = float(arr[0])
		self.y = float(arr[1])

	def dist(self, p):
		return math.sqrt(math.pow(self.x - p.x, 2) + math.pow(self.y - p.y, 2))

	def __str__(self):
		return str(self.x) + " " + str(self.y)

	def __repr__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def nextNear(self, base):
		nearDist = 0
		nearP = 0
		for p in base:
			if p.mark:
				continue
			dist = self.dist(p)
			if nearDist == 0 or dist < nearDist:
				nearDist = dist
				nearP = p

		if nearP == 0:
			return []

		nearP.mark = True
		return [nearP]


def getDist(A, B, C):
	return A.dist(C) + C.dist(B) - A.dist(B)

# base = all points NOT in current hull
def getSmallerDist(A, B, base):
	smallerDist = 0;
	nearP = 0
	for e in base:
		dist = getDist(A, B, e)
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
	for index in range(len(hull) - 1):
		neighbours[(hull[index], hull[index + 1])] = createNeighbour(hull[index], hull[index + 1], free)

	neighbours[(hull[0], hull[len(hull) - 1])] = createNeighbour(hull[0], hull[len(hull) - 1], free)
	return neighbours

def createNeighbour(A, B, free):
	return getSmallerDist(A, B, free)

def addPoint(hull):
	# parcours dict
	# find lowest dist
	# ajoute point
	# supprime old association of dict
	# ajoute 2 nouvelles association
	# check if another el in dict had this point
	# if yes recalculate
	1 + 1

# Read stdin
nbr = int(input())

# create list of Point
base = [Point(input().split(' ')) for i in range(nbr)]
# create list of tuple
#base = [tuple(float(i) for i in input().split(' ')) for i in range(nbr)]

hull = chP(base)
# free = [ x for x in base if x not in hull ]
free = set(base) - set(hull)

neighbours = createAllNeighbours(hull, free)

print(neighbours)
# Print
print(nbr)
print(base)
#[print(e) for e in final]




# def buildNextList(base, p):
# 	pNext = p.nextNear(base)
# 	if len(pNext) == 0:
# 		return []
# 	return pNext + buildNextList(base, p)

# def nextNearSearch(base):
# 	randIndex = random.randrange(len(base))
# 	cur = base[randIndex]
# 	cur.mark = True
# 	return [cur] + buildNextList(base, cur)

# def distFullRoute(base):
# 	fullRoute = base[:]
# 	first = fullRoute.pop(0)
# 	fullDist = sumDist(fullRoute, first, fullRoute[1])
# 	return fullDist + first.dist(base[len(base)-1])

# def sumDist(base, p, curP):
# 	if len(base) == 0:
# 		return 0
# 	nextP = base.pop(0)
# 	return p.dist(curP) + sumDist(base, curP, nextP)