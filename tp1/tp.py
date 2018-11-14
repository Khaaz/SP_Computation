import random
import time
import math

def primaryBinpacking(t, nbr, capacity):
	minBox = math.ceil(nbr / capacity)

def binpacking(t, nbr, capacity):
	bins = []
	
	while t:
		cur = 0
		
		# box with capacity = c
		box = []

		# complete box to be closer to capacity max (c)
		for elem in t:
			if cur + elem <= capacity:
				box.append(elem)
				cur += elem

		# remove in list
		for elem in box:
			t.remove(elem)

		bins.append(box)
	return bins

def optiBinpacking(bins, capacity, startTime):
	i = 0
	while time.time() - startTime < 60:
		randIndex = random.randrange(len(bins))
		
		cur = bins.pop(randIndex)
		cur.sort(reverse=True)

		for b in bins:
			for elem in cur:
				if sum(b) + elem <= capacity:
					b.append(elem)
					cur.remove(elem)

		if cur:
			bins.append(cur)

		i += 1
	return bins

def optiBinpackCleaned(bins, capacity, startTime):
	# Remove all box already full
	tempBins = []
	while sum(bins[0]) == capacity:
		tempBins.append(bins.pop(0))

	#
	bins = optiBinpacking(bins, capacity, startTime)

	# sync bins with tempBins
	for b in tempBins:
		bins.append(b)

	return bins

# setup
startTime = time.time()
random.seed(123456789)

# Read stdin
nbr = int(input())
capacity = int(input())

# create list
t = [int(input()) for i in range(nbr)]

# sort list
t.sort(reverse=True)

#bins = primaryBinpacking()
bins = binpacking(t, nbr, capacity)

bins.sort(key=sum, reverse=True)
if nbr < 1000:
	bins = optiBinpackCleaned(bins, capacity, startTime)
else:
	bins = optiBinpacking(bins, capacity, startTime)

# Print
print(len(bins))
for b in bins:
	[print(e) for e in b]
	print(" ")
