from math import sqrt

def reconstructPath(prevs):
    prevs = prevs[::-1]
    path = []
    next_spot = prevs[0][1]
    for i in prevs:
        i = i[::-1]
        if i[0] == next_spot:
            path.append(i[0])
            next_spot = i[1]

    return path

def h(start, end):
        return sqrt(((start[0] - end[0])**2)+ ((start[1] - end[1])**2))

# From start to goal (len 2 list), H is higher order func, can be anything, dist from goal
def A_star_calc(start, end, h):
    openset = [start]
    reversePath = []
    n = 100

    # g is cost from start to n
    g = [[100.0 for j in range(n)] for i in range(n)]
    g[start[0]][start[1]] = 0

    # f is their sum for a node, overall cost
    f = [[100.0 for j in range(n)] for i in range(n)]
    f[start[0]][start[1]] = h(start, end)



    while openset:
        smallest = 100
        current = None
        for i in openset:
            if f[i[0]][i[1]] < smallest:
                smallest = f[i[0]][i[1]]
                current = i

        if current == end:
            path = reconstructPath(reversePath)
            path.append(start)
            return path

        openset.remove(current)
        neighbors = []

        if current[0] > 0:
            neighbors.append([current[0] - 1, current[1]])
            if current[1] > 0:
                neighbors.append([current[0] - 1, current[1] - 1])
            if current[1] < n - 1:
                neighbors.append([current[0] - 1, current[1] + 1])
        if current[1] > 0:
            neighbors.append([current[0], current[1] - 1])
        if current[0] < n - 1:
            neighbors.append([current[0] + 1, current[1]])
            if current[1] > 0:
                neighbors.append([current[0] + 1, current[1] - 1])
            if current[1] < n - 1:
                neighbors.append([current[0] + 1, current[1] + 1])
        if current[1] < n - 1:
            neighbors.append([current[0], current[1] + 1])

        for i in neighbors:
            temp_g = g[current[0]][current[1]] + 1
            if temp_g < g[i[0]][i[1]]:
                '''
                replaced = False
                for j in reversePath:
                    if j[0] == current:
                        j[1] = i
                        replaced = True
​
                if not replaced:
                '''
                reversePath.append([current, i])

                g[i[0]][i[1]] = temp_g
                f[i[0]][i[1]] = temp_g + h(i, end)
                if i not in openset:
                    openset.append(i)


list = A_star_calc([0, 0], [57, 22], h)
print(list)
array = [[0 for i in range(60)] for j in range(60)]
for x in list:
    array[x[0]][x[1]] = 1
print("\n   ", end="")
for i in range(10):
    print(i, " ", end="")
for i in range(10, 100):
    print(i, "", end="")
print("\n   ", end="")
for i in range(100):
    print("===", end="")
print("")
for n, i in enumerate(array):
    if n < 10:
        print("{} |".format(n), end="")
    else:
        print("{}|".format(n), end="")
    for j in i:
        if j == 0:
            code = "  "
            # code = "_|"
        else:
            code = "X "
            # code = "X|"
        print("{} ".format(code), end="")
    print()