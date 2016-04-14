costs = dict()
matrix = dict()

# -1 ... not possible
costs[(0,0)] = (3,1)
costs[(1,0)] = (3,0)
costs[(2,0)] = (-1,2)

costs[(0,1)] = (3,4)
costs[(1,1)] = (2,6)
costs[(2,1)] = (-1,5)

costs[(0,2)] = (0,-1)
costs[(1,2)] = (7,-1)
costs[(2,2)] = (-1,-1)

def R(i,j):
    return costs[(i,j)][0]

def D(i,j):
    return costs[(i,j)][1]

def C(i,j):
    if (i,j) in matrix.keys():
        return matrix[(i, j)]

    return 0


for i in range(1,3):
    for j in range(1,3):
        cr = C(i-1, j) + R(i-1, j)
        cd = C(i, j-1) + D(i, j-1)

#        print (i,j,cr,cd)

        matrix[(i,j)] = max(cr, cd)

print(matrix)