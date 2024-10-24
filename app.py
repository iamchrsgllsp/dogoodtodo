from functools import wraps
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

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

@app.route('/api/<call>')
@check_dart
def apicall(call):
    match call:
        case "create":
            return "create route"
        case _:
            return "unknown call"

@app.route('/api/post/<task>')
@check_dart
def taskpost(task):
    returnText = f"{task} has been created"
    return {"data": returnText}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
