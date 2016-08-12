#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, stream_with_context, request, Response
from flask.ext.cors import CORS, cross_origin
import os
import json
import search
import sys
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return "<a href='http://www.raulastorga.hol.es'>Ir a mi Currículum</a>"

@app.route('/stream/<string:texto>')
@cross_origin()
def Stream(texto):
    if texto[:2] == "-%":
        texto=texto.replace("-%", "#")
    a = json.dumps(search.TiempoReal(texto))
    return a

@app.route('/usuario/<string:texto>')
@cross_origin()
def Usuario(texto):
    a = json.dumps(search.Usuario(texto))
    return a

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
