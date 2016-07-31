from flask import Flask, stream_with_context, request, Response
import os
import json
import TiempoReal
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hola"

@app.route('/stream/<string:texto>')
def PredecirUsuario(texto):
    return Response(TiempoReal.Inicio(texto))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
