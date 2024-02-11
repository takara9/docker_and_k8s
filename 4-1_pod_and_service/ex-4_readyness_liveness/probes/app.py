from flask import Flask, Response
import json
import signal
import sys

liveness = 0
readiness = 1
app = Flask(__name__)

# 終了シグナル処理
def sighandler(signum, frame):
    print('Signal handler called with signal', signum)
    sys.exit()

signal.signal(signal.SIGTERM, sighandler)

@app.route("/fail")
def fail():
    global liveness
    liveness = 1
    return Response(response=json.dumps({'message': 'switch failed'}), status=200)


@app.route("/be_ready")
def br_ready():
    global readiness
    readiness = 0
    return Response(response=json.dumps({'message': 'status ready'}), status=200)


@app.route("/healthz")
def livenessProbe():
    global liveness
    msg = "OK"
    if liveness == 0:
        result = 200
    else:
        msg = "NG"
        result = 500
    return Response(response=json.dumps({'message': "liveness " + msg}), status=result)


@app.route("/readiness")
def readinessProbe():
    global readiness
    msg = "OK"
    if readiness == 0:
        result = 200
    else:
        msg = "NG"
        result = 500
    return Response(response=json.dumps({'message': 'readiness ' + msg}), status=result)

#app.run()