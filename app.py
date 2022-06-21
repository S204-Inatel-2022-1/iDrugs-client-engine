import os

from flask import request, Blueprint, jsonify
from flask_cors import CORS

from config import app
from service.client import create_user, find_user, delete_user, find_user_login

blueprint = Blueprint('app', __name__, url_prefix='/idrugs-client-engine')

CORS(app)


# CLIENT
@blueprint.route('/client', methods=['POST', 'PUT'])
def create_user_route():
    response = request.json
    return create_user(response)


@blueprint.route('/client', methods=['GET'])
def find_user_route():
    return find_user(request.json)

@blueprint.route('/client/login', methods=['GET'])
def find_user_login_route():
    response = request.json
    return find_user_login(response)


@blueprint.route('/client', methods=['DELETE'])
def delete_user_route():
    response = request.json
    return delete_user(response)


@blueprint.route('/')
def status():
    return jsonify({"message": "IDRUGS-CLIENT-ENGINE: Aplicação rodando"})


app.register_blueprint(blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8082))
    app.run(host='0.0.0.0', port=port)
