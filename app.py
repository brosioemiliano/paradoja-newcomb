import os
import psycopg2
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__, template_folder='../FRONTEND')
app.secret_key = 'clave_secreta_super_segura'

# Leemos la URL de la base de datos de las variables de entorno (Render las cargará)
DATABASE_URL = os.environ.get('DATABASE_URL')

def init_db():
    # Creamos la tabla si no existe
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    # SERIAL es el equivalente a autoincrement en Postgres
    cur.execute('CREATE TABLE IF NOT EXISTS votos (id SERIAL PRIMARY KEY, eleccion TEXT)')
    conn.commit()
    cur.close()
    conn.close()

# Iniciamos la DB al arrancar
init_db()

@app.route('/votar', methods=['POST'])
def votar():
    if session.get('ya_voto'):
        return jsonify({"status": "error", "message": "¡Ya has participado!"}), 403

    data = request.json
    eleccion = data.get('opcion')

    if eleccion in ['ambas', 'caja_a']:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        # ¡OJO! Postgres usa %s, no ?
        cur.execute("INSERT INTO votos (eleccion) VALUES (%s)", (eleccion,))
        conn.commit()
        cur.close()
        conn.close()
        
        session['ya_voto'] = True
        return jsonify({"status": "éxito", "message": "Gracias por votar"}), 200
    
    return jsonify({"status": "error", "message": "Opción inválida"}), 400

# ... resto de tu código
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)