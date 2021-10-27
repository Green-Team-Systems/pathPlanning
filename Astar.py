import dijkstar
import math

class Astar():
    def __init__(self):
        self.graph = dijkstar.Graph(undirected=True)

    def DApath(self, start, end):
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
                            self.graph.add_node((i, j, k), {(i, j - 1, k): 1, (i, j, k - 1): 1, (i, j - 1, k - 1): math.sqrt(2)})
                        elif j == 0:
                            self.graph.add_node((i, j, k), {(i - 1, j, k): 1, (i, j, k - 1): 1, (i - 1, j, k - 1): math.sqrt(2)})
                        elif k == 0:
                            self.graph.add_node((i, j, k), {(i - 1, j, k): 1, (i, j - 1, k): 1, (i - 1, j - 1, k): math.sqrt(2)})
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


