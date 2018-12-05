

class Sommet():
	id = 0
	arrete = []
	dominant = False
	domine = False
	def __init__(self, id):
		self.id = int(id)

	def addArrete(self, sommet):
		self.arrete.append(sommet)

	def markDominant(self):
		self.dominant = True
		self.domine = True
		for som in self.arrete:
			som.domine = True

	def __str__(self):
		return str(self.id) + ' => ' + ', '.join([str(e.id) for e in self.arrete]) + ';'

	def __repr__(self):
		return str(self.id) + ' => ' + ', '.join([str(e.id) for e in self.arrete]) + ';'

# Send back False if at least one is not domine
def checkDomine(graph):
	for elem in graph:
		if elem.domine == False:
			return False
	return True

def listDominant(base):
	final = []
	for elem in base:
		if elem.dominant:
			final.append(elem)
	return final
		
def initGraph(nbArr, graph):
	# create sommet + init list
	for _ in range(nbArr):
		print(graph)
		print('========== ITER ==========')
		(A,B) = tuple(int(j) for j in input().split(' '))
		somA = graph[A]
		somB = graph[B]
		print(somA)
		print(somB)
		if somA == 0:
			somA = Sommet(A)
			graph[A] = somA
			print('somA')
			print(somA)
		if somB == 0:
			somB = Sommet(B)
			graph[B] = somB
			print('somB')
			print(somB)

		somA.addArrete(somB)
		somB.addArrete(somA)

graph = []

nbSommet = int(input())
nbArr = int(input())

# Init empty list
for _ in range(nbSommet):
	graph.append()

initGraph(nbArr, graph)

# for elem in graph:
# 	print('hi')
# 	print(elem.id)
# 	print(len(elem.arrete))
# 	[print(e.id) for e in elem.arrete]
# 	print('=====')
# 	[print(e.id) for e in elem.arrete]
# 	print('=====')

while not checkDomine(graph):
	arrMax = 0
	for elem in graph:
		if elem.dominant: continue
		if len(elem.arrete) > arrMax:
			arrMax = len(elem.arrete)

	for elem in graph:
		if elem.dominant: continue
		if len(elem.arrete) == arrMax:
			elem.markDominant()

final = listDominant(graph)
print(str(len(final)))
[print(e.id) for e in final]





