import signal
import sys
import time
from flask import Flask

# ログ保存
def logger(msg):
    f = open('/app/app.log', 'a')
    f.write(msg)
    f.close()

# シグナルを受けた時の処理
def handler(signum, frame):
    # ここにアプリケーションの終了処理を書く
    logger("Accept SIGNAL\n")
    logger("\n")
    time.sleep(5)
    # コンテナ終了
    sys.exit()

# シグナルSIGTERMを受けた時の処理先関数を定義
signal.signal(signal.SIGTERM, handler)

# Webサービス
app = Flask(__name__)
logger("Start Web service\n")
@app.route("/ping")
def webservice1():
    return "PONG!"
