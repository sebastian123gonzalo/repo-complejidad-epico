import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import time

class Heap():
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left
        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right
        if smallest != idx:
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
            self.swapMinHeapNode(smallest, idx)
            self.minHeapify(smallest)

    def extractMin(self):
        if self.isEmpty():
            return

        root = self.array[0]
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
        self.size -= 1
        self.minHeapify(0)
        return root

    def isEmpty(self):
        return self.size == 0

    def decreaseKey(self, v, dist):
        i = self.pos[v]
        self.array[i][1] = dist

        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
            self.pos[self.array[i][0]] = (i - 1) // 2
            self.pos[self.array[(i - 1) // 2][0]] = i
            self.swapMinHeapNode(i, (i - 1) // 2)
            i = (i - 1) // 2

    def isMinHeap(self, v):
        return self.pos[v] < self.size

class GraphWithPrim():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, src, dest, weight):
        newNode = [dest, weight]
        self.graph[src].append(newNode)  # Use append instead of insert for correct order
        newNode = [src, weight]
        self.graph[dest].append(newNode)  # Use append instead of insert for correct order

    def prim(self):
        V = self.V
        key = [float('inf')] * V  # Initialize all keys as infinite
        parent = [-1] * V  # Array to store constructed MST
        minheap = Heap()

        for v in range(V):
            minheap.array.append(minheap.newMinHeapNode(v, key[v]))
            minheap.pos.append(v)

        minheap.pos[0] = 0
        key[0] = 0
        minheap.decreaseKey(0, key[0])
        minheap.size = V

        mst_edges = []

        while not minheap.isEmpty():
            newMinHeapNode = minheap.extractMin()
            u = newMinHeapNode[0]

            for adj in self.graph[u]:
                v = adj[0]
                weight = adj[1]
                if minheap.isMinHeap(v) and weight < key[v]:
                    key[v] = weight
                    minheap.decreaseKey(v, key[v])
                    parent[v] = u

        for i in range(1, V):
            if parent[i] != -1:  # Asegurarse de que haya un padre para evitar -1
                mst_edges.append((parent[i], i, key[i]))

        return mst_edges

def prim(df):
    matplotlib.use('Agg')
    # Crear el grafo basado en el dataset
    num_vertices = df['Source.IP'].nunique()
    g = GraphWithPrim(num_vertices)

    # Crear un mapeo de las IPs a índices para asegurar que funcione con números
    ip_mapping = {ip: idx for idx, ip in enumerate(df['Source.IP'].unique())}

    for _, row in df.iterrows():
        src_idx = ip_mapping[row['Source.IP']]
        dest_idx = ip_mapping[row['Destination.IP']]
        g.add_edge(src_idx, dest_idx, row['Flow.Bytes.s'])

    # Se ejecuta el algoritmo de Prim y se mide el tiempo de ejecución
    start_time = time.time()
    mst_result = g.prim()
    algorithm_time = time.time() - start_time

    G = nx.Graph()

    for u, v, weight in mst_result:
        G.add_edge(u, v, weight=weight)

    print("Grafo con Prim")
    print(G)

    # Inicio del tiempo de dibujo
    start_time = time.time()

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.3)  # Puedes ajustar el valor de k para separar los nodos
    nx.draw(G, pos, with_labels=False, node_size=10, node_color='blue', edge_color='orange')

    plt.savefig('static/images/prim.png')
    plt.close()

    # Tiempo total de dibujo
    drawing_time = time.time() - start_time

    return G.number_of_edges(), algorithm_time, drawing_time, 'static/images/prim.png'
