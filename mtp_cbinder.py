costs = dict()
matrix = dict()

# -1 ... not possible

#costs[(i,j)] = (L,D) # i is horizontal, j is vertical

costs[(0,0)] = (3,1)
costs[(1,0)] = (3,0)
costs[(2,0)] = (None,2)

costs[(0,1)] = (3,4)
costs[(1,1)] = (2,6)
costs[(2,1)] = (None,5)

costs[(0,2)] = (0,None)
costs[(1,2)] = (7,None)
costs[(2,2)] = (None,None)

def R(i,j):
    return costs[(i,j)][0]

def D(i,j):
    return costs[(i,j)][1]

def C(i,j):
    if (i,j) in matrix.keys():
        return matrix[(i, j)]

    return 0

width = 3
height = 3

for i in range(0,width):
    l = "+"
    for j in range(0,height):
        l+="--" + str(costs[(i,j)][0]) + "--+" #invert i and j!!!
    print(l)



for i in range(0,width):
    for j in range(0,height):
        cr = C(i-1, j) + R(i-1, j) if i > 0 else 0
        cd = C(i, j-1) + D(i, j-1) if j > 0 else 0

        print("i", i, "j", j, "cr", cr, "cd", cd)

        matrix[(i,j)] = max(cr, cd)

print(matrix)