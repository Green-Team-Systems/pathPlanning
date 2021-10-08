import dijkstar

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
                    if i == 0 and j == 0 and k == 0:
                        self.graph.add_node((i, j, k))
                    elif i == 0 and j == 0:
                        self.graph.add_node((i, j, k), {(i, j, k - 1): 1})
                    elif i == 0 and k == 0:
                        self.graph.add_node((i, j, k), {(i, j - 1, k): 1})
                    elif j == 0 and k == 0:
                        self.graph.add_node((i, j, k), {(i - 1, j, k): 1})
                    elif i == 0:
                        self.graph.add_node((i, j, k), {(i, j - 1, k): 1, (i, j, k - 1): 1})
                    elif j == 0:
                        self.graph.add_node((i, j, k), {(i - 1, j, k): 1, (i, j, k - 1): 1})
                    elif k == 0:
                        self.graph.add_node((i, j, k), {(i - 1, j, k): 1, (i, j - 1, k): 1})
                    else:
                        self.graph.add_node((i, j, k), {(i, j - 1, k): 1, (i - 1, j, k): 1, (i, j, k - 1): 1})
        return dijkstar.find_path(self.graph, tuple(start), tuple(end)).nodes

