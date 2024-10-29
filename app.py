from flask import Flask, render_template, request
import pandas as pd
from scripts.kruskal import kruskal
from scripts.prim import prim
from scripts.create_graph import create_graph
from scripts.compare_algorithms import compare_algorithms
import time

app = Flask(__name__)

def measure_time(algorithm, df):
    start_time = time.time()
    edges, algorithm_time, path = algorithm(df)
    drawing_time = time.time() - start_time
    return edges, algorithm_time, drawing_time, path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualization', methods=['POST'])
def optimize():
    # Leer el dataset
    df = pd.read_csv('dataset.csv')

    # Obtener el tipo de algoritmo seleccionado
    algorithm = request.form.get('algorithm')

    if algorithm == 'original':
        edges, time, path = create_graph(df)
        return render_template('index.html',
                                edges_count=edges, 
                                image_load_time=time,
                                image_path=path)
    elif algorithm == 'kruskal':
        edges, algorithm, drawing, path = kruskal(df)
        return render_template('index.html',
                               algorithm_name='Kruskal',
                               edges_count=edges,
                               image_load_time=drawing,
                               algorithm_load_time=algorithm,
                               image_path=path)
    elif algorithm == 'prim':
        edges, algorithm, drawing, path = prim(df)
        return render_template('index.html',
                               algorithm_name='Prim',
                               edges_count=edges,
                               image_load_time=drawing,
                               algorithm_load_time=algorithm,
                               image_path=path)
    elif algorithm == 'compare':
        comparison_results = compare_algorithms(df)
        return render_template('compare_algorithms.html',
                               kruskal_details=comparison_results['kruskal_details'],
                               prim_details=comparison_results['prim_details'])
         
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)