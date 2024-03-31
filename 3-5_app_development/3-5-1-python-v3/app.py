import signal
import sys
from flask import Flask

# シグナルを受けた時の処理
def handler(signum, frame):
    # ここにアプリケーションの終了処理を書く
    #
    # コンテナ終了
    sys.exit()

# シグナルSIGTERMを受けた時の処理先関数を定義
signal.signal(signal.SIGTERM, handler)

# Webサービス
app = Flask(__name__)
@app.route("/ping")
def webservice1():
    return "PONG!"
