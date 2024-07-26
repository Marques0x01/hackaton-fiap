from flask import Blueprint, request, jsonify

health_check_blueprint = Blueprint('healthcheck', __name__)

@health_check_blueprint.route('/', methods=['GET'])
def check():
    return jsonify({'mensagem': 'tudo certo'}), 200
