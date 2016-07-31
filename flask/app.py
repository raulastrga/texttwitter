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

@app.route('/usuario/<string:usr>')
def PredecirUsuario(usr):
    return usr

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
