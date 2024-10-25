from functools import wraps
from flask import Flask, request, redirect, render_template, jsonify

app = Flask(__name__)

datalist = [{"name":"get groceries","location":"lurgan","price":50},{"name":"test2","location":"lurgan","price":50}]

def check_dart(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Dart" not in request.headers['User-Agent']:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/dartcheck')
def checker():
    print(request.headers)
    return {"data":200}

@app.route('/api/tasks')
@check_dart
def apicall():
    return jsonify(datalist)

@app.route('/api/post/<task>', methods=["POST"])
@check_dart
def taskpost(task):
    recvd = request.json
    print(recvd['name'])
    datalist.append(recvd)
    returnText = f"{recvd['name']} has been created"
    return {"data": returnText}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
