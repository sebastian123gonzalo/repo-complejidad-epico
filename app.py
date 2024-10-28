from flask import Flask, render_template, request
import pandas as pd
from scripts.kruskal import kruskal
from scripts.prim import prim
from scripts.create_graph import create_graph

app = Flask(__name__)

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
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
