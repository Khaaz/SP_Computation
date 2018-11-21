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


def pickVector(base, final, step):
	result = []
	baseTmp = base

	# sort
	for i in range(int(2 * math.pi * 100)):
		baseTmp.sort(key = lambda p: math.cos(i) * p.x + math.sin(i) * p.y)
		optiGrap(baseTmp, result)
		if len(result) > len(final):
			final = result

	return final


def optiGrap(base, result):
	while base:
		cur = base[0]
		result.append(cur)

		temp = []
		for elem in base:
			if cur.dist(elem) > r:
				temp.append(elem)

		base = temp


# Read stdin
nbr = int(input())
r = float(input())

# create list
base = [Point(input().split(' ')) for i in range(nbr)]
final = []

final = pickVector(base, final, 1)


# print result
print(len(final))
#[print(e) for e in result]

# make sure result validity
ensureResultValidity(final)
