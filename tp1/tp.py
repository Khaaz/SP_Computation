def binpacking1(t, nbr, capacity):
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

nbr = int(input())
capacity = int(input())

# create list
t = [int(input()) for i in range(nbr)]

# sort list
t.sort(reverse=True)
bins = binpacking1(t, nbr, capacity)

print(len(bins))
#print(bins)
