from functools import wraps
from flask import Flask, request, redirect, render_template, jsonify

app = Flask(__name__)


testStart = False
testComplete = False
datalist = [{"name":"1st task","description":"testing out functionality","location":"Lurgan","price":50}]

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

@app.route('/api/flagswitch', methods=['GET'])
def flagswitch():
    global testComplete
    global testStart

    # Toggle the flags
    testStart = not testStart
    testComplete = not testComplete

    return {"data": f"{testStart} and {testComplete}"}

@app.route('/api/user/active')
@check_dart
def getActive():
    return {"data":{"task":123,"isStarted":testStart,"isCompleted":testComplete}}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
