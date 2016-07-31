from flask import Flask
import os
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/")
def main():
    return "Welcome!"

@app.route('/usuario', methods=['POST'])
def PredecirUsuario():
    #Cargar valores
    _usr = request.form['usr']

    # validate the received values
    if _usr:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
