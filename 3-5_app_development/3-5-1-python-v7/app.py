import os
import signal
import sys
import time
import json
from socket import gethostname, gethostbyname
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import pymysql
pymysql.install_as_MySQLdb()

# 環境変数の取り込み関数
def loadenv(envvar, default):
    w = os.environ.get(envvar)
    if w is None:
        w = default
    return w

# 環境変数の取り込み
db_database = loadenv('MARIADB_DATABASE','mydb') 
db_root_passwd = loadenv('MARIADB_ROOT_PASSWORD','secret0')
db_host = loadenv('MARIADB_HOST','mariadb') 
db_port = loadenv('MARIADB_PORT','3306')
db_user = loadenv('MARIADB_USER','user1')
db_user_passwd = loadenv('MARIADB_PASSWORD','secret1')
db_con = 'mysql+pymysql://' + db_user + ':' + db_user_passwd + '@' + db_host  + ':' + db_port  + '/' + db_database

# Webサービス
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_con
db = SQLAlchemy(app)
ma = Marshmallow()

## モデル
class Person(db.Model):
    __tablename__ = 'Persons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return "<Person(Firt name='%s',Last name'%s')>" % (self.first_name, self.last_name)

    # 登録
    def recPerson(person):
        record = Person(
            first_name=person['fname'],
            last_name=person['lname'],
        )
        db.session.add(record)
        db.session.commit()
        return person

    # IDで名前取得
    def getPersonById(id):
        person = Person.query.get(id)
        return person

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name')

# ログ保存
def logger(msg):
    f = open('/app/app.log', 'a')
    f.write(msg)
    f.close()

# シグナルを受けた時の処理
def handler(signum, frame):
    # ここにアプリケーションの終了処理を書く
    ## KubernetesからSIGTERMが来ると、それ以降はリクエストが転送されない。
    logger("Accept SIGNAL\n")
    # コンテナ終了 ここで終了しない
    ## sys.exit()

# シグナルSIGTERMを受けた時の処理先関数を定義
signal.signal(signal.SIGTERM, handler)


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


# レディネスプローブ　実装したい
@app.route('/rediness/', methods=['GET'])
def rediness():
    return Response(response=json.dumps({'message': 'ok'}), status=200)

# ライブネスプローブ　実装したい
@app.route('/healthz/', methods=['GET'])
def healthz():
    return Response(response=json.dumps({'message': 'ok'}), status=200)

## コントローラー
# 登録 データの返し方を再考慮
@app.route('/person/', methods=['POST'])
def recPerson():
    reqData = json.dumps(request.json)
    personData = json.loads(reqData)
    person = Person.recPerson(personData)
    person_schema = PersonSchema()
    return jsonify(person_schema.dump(person))

# ユーザー情報取得
@app.route('/person/<string:id>/', methods=['GET'])
def getPerson(id):
    person = Person.getPersonById(id)
    person_schema = PersonSchema()
    if person == {}:
        return jsonify({})
    return make_response(jsonify(person_schema.dump(person)))


if __name__ == "__main__":
    app.run(debug=True)
