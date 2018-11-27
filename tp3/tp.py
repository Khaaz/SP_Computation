import random

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

	def nextNear(base):
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


def buildNextList(base, p):
	pNext = p.nextNear(base)
	if len(pNext) == 0:
		return
	return pNext + buildNextList(base, p)

def nextNearSearch(base):
	randIndex = random.randrange(len(base))
	cur = base[randIndex]
	cur.mark = True
	return [cur] + buildNextList(base, cur)

def distFullRoute(base):
	fullRoute = base
	first = fullRoute.pop(0)
	fullDist = sumDist(base, first, fullRoute[1])
	return fullDist + first.dist(base[len(base)])

def sumDist(base, p, curP):
	if len(base) == 0:
		return 0
	nextP = base.pop(0)
	return p.dist(curP) + sumDist(base, curP, nextP)


# convex hull from tuple
def ch(v):
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
def ch(v):
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

# Read stdin
nbr = int(input())

# create list of Point
base = [Point(input().split(' ')) for i in range(nbr)]
# create list of tuple
#base = [tuple(float(i) for i in input().split(' ')) for i in range(nbr)]

print(base)

final = nextNearSearch(base)
fulldist = distFullRoute(base)

print(final)
print(fulldist)
