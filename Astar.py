import dijkstar
import math
import numpy as np
from os.path import exists


class Astar():
    #xC = lambda n, a, b: n/(a * b) # lambda function for calculating x from index, size of x coord, size of z coord.
    #yC = lambda n, a, b: (n/b) % a # lambda function for calculating y from index, size, of x coord, size of z
    #zC = lambda n, a: n % a # lambda function for calculating z from index, size of z coord.


    def __init__(self):
        self.graph = dijkstar.Graph(undirected=True)

    def DApath(self, start, end, filename, size):
        if exists(filename):
            grid = np.load(filename)
            n = -size[0] + size[1]
            m = -size[2] + size[3]
            o = -size[4] + size[5]
            for i in range(n*m*o): # false if open, true if closed
                if(grid[i]):
                    pass
                else:
                    xC = i//(n * o)
                    yC = (i//o) % n
                    zC = i % o
                    xstat = xC != 1
                    ystat = yC != 1
                    zstat = zC != 1
                    if(xstat and not grid[i - m * o]): 
                        self.graph.add_edge((xC, yC, zC), (xC - 1, yC, zC), 1)
                        # print('edge added at', xC, 'and', yC ,' and ', zC)
                    if(ystat and not grid[i - o]): self.graph.add_edge((xC, yC, zC), (xC, yC - 1, zC), 1)
                    if(zstat and not grid[i - 1]): 
                        self.graph.add_edge((xC, yC, zC), (xC, yC, zC - 1), 1)
                        # print('z edge added at', xC, 'and', yC ,' and ', zC)
                    if(xstat and zstat and not grid[i - (m * o) - 1]): self.graph.add_edge((xC, yC, zC), (xC - 1, yC, zC - 1), math.sqrt(2))
                    if(xstat and ystat and not grid[i - (m * o) - o]): self.graph.add_edge((xC, yC, zC), (xC - 1, yC - 1, zC), math.sqrt(2))
                    if(ystat and zstat and not grid[i - o - 1]): self.graph.add_edge((xC, yC, zC), (xC, yC - 1, zC - 1), math.sqrt(2))
                    if(xstat and ystat and zstat and not grid[i - (m * o) - o - 1]): self.graph.add_edge((xC, yC, zC), (xC - 1, yC - 1, zC - 1), math.sqrt(3))
            return dijkstar.find_path(self.graph, tuple(start), tuple(end)).nodes
        else:
            n = end[0] + 10
            m = end[1] + 10
            o = end[2] + 10
            for i in range(n):
                for j in range(m):
                    for k in range(o):
                        if 40 <= i and i <= 64 and 98 <= j and j <= 120:
                            pass
                        if 30 <= i and i <= 45 and 30 <= j and j <= 45:
                            pass
                        else:
                            if i == 0 and j == 0 and k == 0:
                                self.graph.add_node((i, j, k))
                            elif i == 0 and j == 0:
                                self.graph.add_node((i, j, k), {(i, j, k - 1): 1})
                            elif i == 0 and k == 0:
                                self.graph.add_node((i, j, k), {(i, j - 1, k): 1})
                            elif j == 0 and k == 0:
                                self.graph.add_node((i, j, k), {(i - 1, j, k): 1})
                            elif i == 0:
                                self.graph.add_node(
                                    (i, j, k), {(i, j - 1, k): 1, (i, j, k - 1): 1, (i, j - 1, k - 1): math.sqrt(2)})
                            elif j == 0:
                                self.graph.add_node(
                                    (i, j, k), {(i - 1, j, k): 1, (i, j, k - 1): 1, (i - 1, j, k - 1): math.sqrt(2)})
                            elif k == 0:
                                self.graph.add_node(
                                    (i, j, k), {(i - 1, j, k): 1, (i, j - 1, k): 1, (i - 1, j - 1, k): math.sqrt(2)})
                            else:
                                self.graph.add_node((i, j, k),
                                                    {
                                    (i - 1, j, k): 1,
                                    (i, j - 1, k): 1,
                                    (i, j, k - 1): 1,
                                    (i, j - 1, k - 1): math.sqrt(2),
                                    (i - 1, j, k - 1): math.sqrt(2),
                                    (i - 1, j - 1, k): math.sqrt(2),
                                    (i - 1, j - 1, k - 1): math.sqrt(3)
                                }
                                )
            return dijkstar.find_path(self.graph, tuple(start), tuple(end)).nodes
        

