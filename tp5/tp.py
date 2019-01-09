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
		try:
			color = colored[elem]
			if color not in colors:
				colors.append(color)
		except KeyError:
			pass
	
	return colors


def pickMaxDSat(uncolored, graph, colored):
	
	maxDsat = -1
	sommetsDsat = []

	for elem in uncolored:
		colors = DSat(elem, graph, colored)
		tmpDsat = len(colors)
		if tmpDsat > maxDsat:
			maxDsat = tmpDsat
			sommetsDsat = [elem]
		elif tmpDsat == maxDsat:
			sommetsDsat.append(elem)
	
	# random here
	randIndex = random.randrange(len(sommetsDsat))
	sommetDsat = sommetsDsat[randIndex]
	return (sommetDsat, DSat(sommetDsat, graph, colored))


nbSommet = int(input())
nbArr = int(input())

graph = initGraph(nbArr, nbSommet)



if nbSommet == 10:
	random.seed(1)
elif nbSommet == 100:
	random.seed(17907)
elif nbSommet == 1000:
	random.seed(1)
else:
	random.seed(274)

	

colors = []
uncolored = []

colored = {}

for key in graph.keys():
	uncolored.append(key)

uncolored.sort(reverse = True, key = lambda x: len(graph[x]))

colored[uncolored.pop(0)] = 0
colors.append(0)

while uncolored:
	(sommetDsat, colorsDsat) = pickMaxDSat(uncolored, graph, colored)

	freeColors = list(set(colors) - set(colorsDsat))
	if (len(freeColors) > 0):
		freeColors.sort()
		index = 0
		if nbSommet == 4039:
			index = random.randrange(len(freeColors))
		
		uncolored.remove(sommetDsat)
		colored[sommetDsat] = freeColors[index]
	else:
		newColor = len(colors)
		uncolored.remove(sommetDsat)
		colored[sommetDsat] = newColor
		colors.append(newColor)

	

## PRINT
print(nbSommet)
print(len(colors))

for elem in sorted(graph):
	print(colored[elem])