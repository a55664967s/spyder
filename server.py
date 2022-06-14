from flask import Flask, Blueprint
from flask_cors import CORS
from flasgger import Swagger
from comic import comic_blueprints
app = Flask(__name__)
CORS(app)
app.register_blueprint(comic_blueprints)

Swagger(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)