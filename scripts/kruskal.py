import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import time

class GraphWithKruskal:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []  # Aquí almacenaremos el MST
        i, e, tot_weight = 0, 0, 0

        # Ordenar los bordes por peso
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        # Crear subconjuntos independientes para cada vértice
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Número de aristas en el MST será igual a V-1
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # Si no forman un ciclo, incluirlos en el MST
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        return result

def kruskal(df):
    matplotlib.use('Agg')
    # Crear un grafo con el número de nodos igual al número de IPs únicas en el dataset
    nodes = pd.concat([df['Source.IP'], df['Destination.IP']]).unique()
    g = GraphWithKruskal(len(nodes))
    
    # Crear un diccionario para mapear las IPs a índices numéricos
    node_map = {node: idx for idx, node in enumerate(nodes)}

    # Añadir las aristas al grafo, mapeando las IPs a sus índices
    for index, row in df.iterrows():
        u = node_map[row['Source.IP']]
        v = node_map[row['Destination.IP']]
        w = row['Flow.Bytes.s']
        g.add_edge(u, v, w)

    # Se ejecuta el algoritmo de Kruskal y se mide el tiempo de ejecución
    start_time = time.time()
    mst_result = g.kruskal()
    algorithm_time = time.time() - start_time

    # Crear el grafo optimizado (MST) utilizando NetworkX para visualizarlo
    G = nx.Graph()
    
    # Añadir las aristas del MST al grafo
    for u, v, weight in mst_result:
        G.add_edge(nodes[u], nodes[v], weight=weight)

    print("Grafo con Kruskal")
    print(G)

    # Inicio del tiempo de dibujo
    start_time = time.time()

    # Dibujar el MST y guardar la imagen
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.3)
    nx.draw(G, pos, with_labels=False, node_size=10, node_color='blue', edge_color='orange')

    plt.savefig('static/images/kruskal.png')  # Guardar la imagen
    plt.close()

    # Tiempo de dibujo total
    drawing_time = time.time() - start_time

    return G.number_of_edges(), algorithm_time, drawing_time, 'static/images/kruskal.png'  # Retornar la ruta de la imagen
