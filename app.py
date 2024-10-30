from functools import wraps
from flask import Flask, request, redirect, render_template, jsonify
from database import create_table, get_inactive_tasks, add_task, accept_task, get_accepted_tasks
from func import format_task_response

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
    print(get_inactive_tasks())
    datalist = format_task_response(get_inactive_tasks())
    return jsonify(datalist)

@app.route('/api/post/<task>', methods=["POST"])
@check_dart
def taskpost(task):
    recvd = request.json
    print(recvd['name'])
    datalist.append(recvd)
    returnText = f"{recvd['name']} has been created"
    task = ("chris",recvd['name'],recvd['description'],recvd['location'],recvd['price'],False)
    print(task)
    add_task(task)
    get_inactive_tasks()
    return {"data": returnText}

@app.route('/api/acceptedtasks')
@check_dart
def getacceptedtaskes():
    datalist = format_task_response(get_accepted_tasks('dave'))
    return jsonify(datalist)

@app.route('/api/accepttask', methods=['POST'])
@check_dart
def accepttask():
    resp = request.json
    accept_task(resp['taskid'],resp['name'])
    return {"data":"yes"}

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
    create_table()
    get_inactive_tasks()
    app.run(debug=True, host="0.0.0.0", port=5000)
