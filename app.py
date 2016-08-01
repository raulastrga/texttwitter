#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, stream_with_context, request, Response
import os
import json
import search
app = Flask(__name__)

@app.route("/")
def hello():
    return "<a href='http://www.raulastorga.hol.es'>Ir a mi Currículum</a>"

@app.route('/stream/<string:texto>')
def Stream(texto):
    a = str(search.TiempoReal(texto))
    return a

@app.route('/usuario/<string:texto>')
def Usuario(texto):
    a = str(search.TiempoReal(texto))
    return a

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
