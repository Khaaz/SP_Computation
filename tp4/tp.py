import random


def initGraph(nbArr):
	graph = {}
	# create sommet + init list
	for _ in range(nbArr):
		
		(A,B) = tuple(int(j) for j in input().split(' '))
		
		somA = graph.get(A)
		somB = graph.get(B)

		if somA == None:
			graph[A] = [B]
		else:
			somA.append(B)

		if somB == None:
			graph[B] = [A]
		else:
			somB.append(A)

	return graph

def process(free, graph, final):
	lowest = None
	low = []
	for key, value in graph.items():
		length = len(value)
		if lowest == None or length < lowest:
			low = [key]
			lowest = length
		elif length == lowest:
			low.append(key)

	lowLen = len(low)

	randIndex = random.randrange(len(low))
	weak = low[randIndex]
	
	neighbours = graph.get(weak)

	highest = None
	high = []
	for n in neighbours:
		elem = graph[n]
		length = len(elem)
		if highest == None or length > highest:
			high = [n]
			highest = length
		elif length == highest:
			high.append(n)

	highLen = len(high)
	strong = weak
	if highLen > 0:
		randIndex = random.randrange(len(high))
		strong = high[randIndex]

	final.append(strong)

	dominates = graph.pop(strong)

	# clean graph
	for value in graph.values():
		try:
			value.remove(strong)
		except ValueError:
			pass
		for elem in dominates:
			try:
				value.remove(elem)
			except ValueError:
				pass

	for elem in dominates:
		try:
			graph.pop(elem)
			#value.remove(elem)
		except ValueError:
			pass
			
	# clean free
	try:
		free.remove(strong)
	except ValueError:
		pass
	
	for elem in dominates:
		try:
			free.remove(elem)
		except ValueError:
			pass
		


nbSommet = int(input())
nbArr = int(input())

graph = initGraph(nbArr)

free = []

# Init list of free point
for key in graph.keys():
	free.append(key)

final = []

while free:
	process(free, graph, final)


print(len(final))
[print(e) for e in final]
