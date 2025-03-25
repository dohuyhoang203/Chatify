import os

from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=None)

@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'chat.png')

@app.route('/static/<path:path>')
def serve_static_file(path):
    return send_from_directory(os.path.join(app.root_path, 'static'), path)

from src.apis.web_blueprints import *

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)