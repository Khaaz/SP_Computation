import random

def initGraph(nbArr, nbSommet):
	graph = {}

	for i in range(nbSommet):
		graph[i] = []
	# create sommet + init list
	for _ in range(nbArr):
		
		A, B = tuple(int(j) for j in input().split(' '))
		
		graph[A].append(B)
		graph[B].append(A)
		
	return graph

def DSat(sommet, graph, colored):
	near = graph[sommet]

	colors = []
	for elem in near:
		color = colored[elem]
		if color not in colors:
			colors.append(color)
	
	return colors


def pickMaxDSat(uncolored, graph, colored):
	
	maxDsat = -1
	sommetsDsat = []
	colorsDsat = None

	for elem in uncolored:
		colors = DSat(elem, graph, colored)
		tmpDsat = len(colors)
		if tmpDsat > maxDsat:
			maxDsat = tmpDsat
			sommetDsat = [elem]
		else if tmpDsat == maxDsat:
			sommetDsat.append(elem)
	
	# random here
	randIndex = random.randrange(len(sommetDsat))
	sommetDsat = sommetsDsat[randIndex]
	return (sommetDsat, DSat(sommetDsat, graph, colored))


nbSommet = int(input())
nbArr = int(input())

# if nbSommet == 16:
# 	random.seed(1)
# elif nbSommet == 256:
# 	random.seed(6)
# elif nbSommet == 1000:
# 	random.seed(1)
# else:
# 	random.seed(1)

graph = initGraph(nbArr, nbSommet)

colors = []
uncolored = []

colored = {}

for key in graph.keys():
	uncolored.append(key)

uncolored.sort(reverse = True, key = lambda x: len(graph[x]))

colored[uncolored.pop(0)] = 1
colors.append(1)

while uncolored:
	(sommetDsat, colorsDsat) = pickMaxDSat(uncolored, graph, colored)

	freeColors = set(colors) - set(colorsDsat)
	if (len(freeColors) > 0)
		freeColors.sort()
		colored[uncolored.remove(sommetDsat)] = freeColors[0]
	else:
		newColor = len(colors) + 1
		colored[uncolored.remove(sommetDsat)] = newColor
		colors.append(newColor)


## PRINT
print(nbSommet)
print(len(colors))

for elem in sorted(graph.iterkeys()):
	print(colored[elem])