
##A = [[0, 1, False],[1, 2, False],[2, 3, False], [3, 2, False], [2, 4, False], [4, 0, False]]

A = [[0, 1, False], [0, 2, False], [1, 2, False], [2, 1, False], [2, 3, False]]

# dont forget that if it is the end it needs to print out the last one too


cursor = 0
for i in range(len(A)):
	print(cursor)

	## find the index where the first value equals the cursor
	found = False
	val = 0
	while not found and val < len(A):
		if A[val][0] == cursor and not A[val][2]:
			found = True
		if not found:
			val += 1

	cursor = A[val][1]
	A[val][2] = True


print(A)

def checkNodes(A):
	nodes = []
	for i in range(len(A)):
		if not A[i][2]:
			nodes.append(i)
	return(nodes)

print(checkNodes(A))


		