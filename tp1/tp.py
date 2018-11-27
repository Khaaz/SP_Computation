import random
import time
import math

# Ping pong function to iterate through a list in order/reverse order
def pingpong(seq):
    seq = list(seq)
    while True:
        yield from seq
        yield from reversed(seq)

# Binpack from sorted list (higher > lower).
# Add higher number in a box + next higher Number
def binpacking(t, capacity):
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

# put numbers in boxes using a better shiffling with ping pong function
def primaryBinpacking(t, nbr, capacity):
	minBox = math.ceil(sum(t) / capacity)

	result = []
	for _ in range(minBox):
		result.append([])

	temp = []
	for num, lst in zip(t, pingpong(result)):
		if (sum(lst) + num) <= capacity:
			lst.append(num)
			temp.append(num)

	for elem in temp:
		t.remove(elem)
	
	return result

# regular binpack algorithm with already created bins list
def binpackingFromPrimary(t, capacity, bins):
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

# break a box and try to recreate. Potentially lower box number/never increase
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

# remove all full boxes before running optiBinpacking
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

# opti binpack without touching already full boxes
def optiBinpackWOFull(bins, capacity, startTime):
	
	i = 0
	while time.time() - startTime < 60:
		bins.sort(key=len)
		randIndex = random.randrange(len(bins))

		# pick another index if the box is already full
		if sum(bins[randIndex]) == capacity:
			continue
		
		cur = bins.pop(randIndex)
		#cur.sort(reverse=True)

		for b in bins:
			for elem in cur:
				if sum(b) + elem <= capacity:
					b.append(elem)
					cur.remove(elem)

		if cur:
			bins.append(cur)

		i += 1
	return bins

# setup
startTime = time.time()
random.seed(1)

# Read stdin
nbr = int(input())
capacity = int(input())

# create list
t = [int(input()) for i in range(nbr)]

# sort list
t.sort(reverse=True)

# Get a result with a better shuffled first result
bins = primaryBinpacking(t, nbr, capacity)
binpackingFromPrimary(t, capacity, bins)

# normal binpack (higher value + next higher value)
#bins = binpacking(t, capacity)

## possible solution
#bins.sort(key=sum, reverse=True)
#bins = optiBinpacking(bins, capacity, startTime)

if nbr == 100:
	random.seed(123456789)
	bins.sort(key=sum, reverse=True)
	bins = optiBinpackCleaned(bins, capacity, startTime)
else :
	# binpack without breaking already full boxes
	bins = optiBinpackWOFull(bins, capacity, startTime)


# Print
print(len(bins))
for b in bins:
	[print(e) for e in b]
	print(" ")
