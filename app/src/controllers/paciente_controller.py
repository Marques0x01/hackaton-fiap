from flask import request, jsonify
from src.services.paciente_service import PacienteService

class PacienteController:

    def __init__(self, service: PacienteService) -> None:
        self.__service = service

    def post_paciente(self):
        data = request.get_json()
        return jsonify(self.__service.cadastrar_paciente(data))
