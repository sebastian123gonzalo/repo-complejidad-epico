import pandas as pd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import time

def create_graph(df):
    matplotlib.use('Agg')
    # Crear un grafo dirigido
    G = nx.Graph()

    # Añadir nodos y aristas al grafo
    for _, row in df.iterrows():
        weight = row['Flow.Bytes.s']
        G.add_edge(row['Source.IP'], row['Destination.IP'], weight=weight)

    # Imprimir el número de nodos creados
    print("Grafo original")
    print(G)

    # Inicio del tiempo de dibujo
    start_time = time.time()

    # Dibujar el grafo y guardar la imagen
    plt.figure(figsize=(12, 10))  # Ajustar el tamaño de la figura
    pos = nx.spring_layout(G, k=0.3)  # Ajustar el parámetro k para acercar los nodos
    nx.draw(G, pos, with_labels=False, node_size=10, node_color='blue', edge_color='orange')

    plt.savefig('static/images/graph.png')  # Guardar la imagen en la carpeta 'static/images'
    plt.close()

    # Tiempo de dibujo total
    drawing_time = time.time() - start_time
    # Se retorna el numero de aristas, el tiempo de dibujo y la ruta de la imagen
    return G.number_of_edges(), drawing_time, 'static/images/graph.png'