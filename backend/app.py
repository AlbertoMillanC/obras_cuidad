from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obras.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de datos para las obras
class Obra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.String(10), nullable=False)
    fecha_fin = db.Column(db.String(10))
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)

# Crear las tablas
with app.app_context():
    db.create_all()

@app.route('/api/obras', methods=['GET'])
def obtener_obras():
    obras = Obra.query.all()
    return jsonify([{
        'id': obra.id,
        'nombre': obra.nombre,
        'descripcion': obra.descripcion,
        'estado': obra.estado,
        'fecha_inicio': obra.fecha_inicio,
        'fecha_fin': obra.fecha_fin,
        'latitud': obra.latitud,
        'longitud': obra.longitud
    } for obra in obras])

@app.route('/api/obras', methods=['POST'])
def crear_obra():
    datos = request.json
    nueva_obra = Obra(
        nombre=datos['nombre'],
        descripcion=datos['descripcion'],
        estado=datos['estado'],
        fecha_inicio=datos['fecha_inicio'],
        fecha_fin=datos.get('fecha_fin'),
        latitud=datos['latitud'],
        longitud=datos['longitud']
    )
    db.session.add(nueva_obra)
    db.session.commit()
    return jsonify({'mensaje': 'Obra creada exitosamente'}), 201

if __name__ == '__main__':
    app.run(debug=True)
