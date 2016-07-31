from flask import Flask
import json
app = Flask(__name__)

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
    app.run()
