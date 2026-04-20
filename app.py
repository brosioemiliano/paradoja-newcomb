from flask import Flask, render_template, request, jsonify, session
import sqlite3

# Ajustamos la ruta de la carpeta de templates hacia la carpeta FRONTEND
app = Flask(__name__, template_folder='../FRONTEND')
app.secret_key = 'clave_secreta_super_segura'

# El archivo de base de datos se guardará en la carpeta BACKEND al ejecutar
DB_NAME = 'encuesta.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('CREATE TABLE IF NOT EXISTS votos (id INTEGER PRIMARY KEY, eleccion TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votar', methods=['POST'])
def votar():
    if session.get('ya_voto'):
        return jsonify({"status": "error", "message": "¡Ya has participado!"}), 403

    data = request.json
    eleccion = data.get('opcion')

    if eleccion in ['ambas', 'caja_a']:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO votos (eleccion) VALUES (?)", (eleccion,))
        conn.commit()
        conn.close()
        
        session['ya_voto'] = True
        return jsonify({"status": "éxito", "message": "Gracias por votar"}), 200
    
    return jsonify({"status": "error", "message": "Opción inválida"}), 400

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)