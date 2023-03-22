import os
import json

from flask import Flask, request, jsonify
from modelo.laberintoBuilder import Director

app = Flask(__name__)

director=Director()
director.procesar('./modelo/lab2hab.json')
juego=director.obtenerJuego()

@app.route("/")
def hello_world():
    #name = os.environ.get("NAME", "World")
    name="Pepe"
    return "Hello {}!".format(name)

@app.route("/numeroHab")
def numeroHab():
    num=juego.numeroHab()
    return "Numero: {}".format(num)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))