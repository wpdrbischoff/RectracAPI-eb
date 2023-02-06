from config.db import DBURL

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from werkzeug.middleware.proxy_fix import ProxyFix

myclient = MongoClient(DBURL)
db = myclient["wpd"]

def get_all_table_data(table):
    Collection = db[table]
    data = Collection.find()
    result = [{item: _[item] for item in _ if item != '_id'} for _ in data]
    return jsonify(result)

def health_checker_func():
    return "<html><p>I'M ALLLLIVE</p></html>"

application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}})

@application.route('/', methods=['GET'])
def health_checker():
    return health_checker_func()

@application.route('/table/<table>', methods=['GET'])
def get_table_data(table):
    return get_all_table_data(table)

application.wsgi_app = ProxyFix(
    application.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    #application.debug = True
    application.run(port=80)
    #application.run(port=1337)
