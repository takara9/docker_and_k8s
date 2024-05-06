import os
import signal
import sys
import time
import json
import logging
from socket import gethostname, gethostbyname
from flask import Flask, request, jsonify, make_response
import mysql.connector

# 環境変数の取り込み関数
def loadenv(envvar, default):
    w = os.environ.get(envvar)
    if w is None:
        w = default
    return w

# 環境変数の取り込みとDB接続
def db_connect():
    try:
        ret = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_database,
            user=db_user,
            password=db_user_passwd
        )
        return ret
    except mysql.connector.Error as err:
        return None

def db_connect_readonly():
    try:
        ret = mysql.connector.connect(
            host=db_readonly_host,
            port=db_port,
            database=db_database,
            user=db_user,
            password=db_user_passwd
        )
        return ret
    except mysql.connector.Error as err:
        print(err)
        sys.exit()
        return None

# シグナルを受けた時の処理
def handler(signum, frame):
    # ここにアプリケーションの終了処理を書く
    ## KubernetesからSIGTERMが来ると、それ以降はリクエストが転送されない。
    logging.debug("Accept SIGNAL\n")
    # ここでコンテナ終了しない事で、終了間際の応答を返す
    ## sys.exit()

##
## MAIN
##
### 環境変数
db_database = loadenv('MARIADB_DATABASE','mydb') 
db_root_passwd = loadenv('MARIADB_ROOT_PASSWORD','secret0')
db_host = loadenv('MARIADB_HOST','mariadb') 
db_readonly_host = loadenv('MARIADB_READONLY_HOST','mariadb')
db_port = loadenv('MARIADB_PORT','3306')
db_user = loadenv('MARIADB_USER','user1')
db_user_passwd = loadenv('MARIADB_PASSWORD','secret1')
### ロギング
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.debug('Start Web Server')
### シグナル
signal.signal(signal.SIGTERM, handler) # シグナル受信時の処理先を定義
### Webサービス
app = Flask(__name__)        # Webサービス
cnx = db_connect()           # データベース接続
cnro = db_connect_readonly()  # 読み取り専用データベース接続

if __name__ == "__main__":
    app.run(debug=True)


# ping応答
@app.route("/ping")
def ws_ping():
    return "PONG!"

# ホスト情報 
@app.route("/info")
def ws_info():
    hostname = gethostname()
    resp = ""
    resp = resp + 'Host Name: %s' % hostname + "\n"
    resp = resp + 'Host IP: %s' % gethostbyname(hostname) + "\n"
    return resp + 'Client IP : %s' % request.remote_addr + "\n"


# レディネスプローブ
@app.route('/readiness', methods=['GET'])
def rediness():
    try:
        cnxx = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database="mysql",
            user="root",
            password=db_root_passwd
        )
        cursor = cnxx.cursor()
        cursor.execute("SELECT * FROM user")
        cnxx.close()
        return jsonify({}), 200
    except mysql.connector.Error as err:
        logging.debug('err:', err)
        return jsonify({}), 500

# ライブネスプローブ
@app.route('/healthz', methods=['GET'])
def healthz():
    try:
        cnxx = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_database,
            user=db_user,
            password=db_user_passwd
        )
        cursor = cnxx.cursor()
        cursor.execute("SELECT id FROM Persons")
        cnxx.close()
        return jsonify({}), 200
    except mysql.connector.Error as err:
        logging.debug('err:', err)
        return jsonify({}), 500


## コントローラー
# 登録 データの返し方を再考慮
@app.route('/person/', methods=['POST'])
def recPerson():
    reqData = json.dumps(request.json)
    personData = json.loads(reqData)
    sql = 'INSERT INTO Persons (first_name, last_name) VALUES ("%s", "%s")' % (personData['fname'], personData['lname'])
    cur = cnx.cursor(buffered=True)    
    cur.execute(sql)
    cnx.commit()
    return request.json, 200

# IDでユーザー情報取得
@app.route('/person/<string:id>/', methods=['GET'])
def getPerson(id):
    cur = cnx.cursor(buffered=True)
    sql = 'SELECT id, first_name, last_name FROM Persons WHERE id = %s' % id
    cur.execute(sql)
    for (did, first_name, last_name) in cur:
        return jsonify({"id": did, "first_name": first_name, "last_name": last_name}), 200

# 全ユーザー情報取得
@app.route('/persons', methods=['GET'])
def getPersons():
    cur = cnro.cursor(buffered=True)
    sql = 'SELECT id, first_name, last_name FROM Persons'
    cur.execute(sql)
    result = []
    for (id, first_name, last_name) in cur:
        result.append({"id": id, "first_name": first_name, "last_name": last_name})
    return jsonify(result), 200


