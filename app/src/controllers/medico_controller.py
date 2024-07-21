from flask import request, jsonify
from services.medico_service import MedicoService

class MedicoController:

    def __init__(self, service: MedicoService) -> None:
        self.__service = service

    def get_medicos(self):
        medicos = self.__service.listar_medicos()
        print(medicos)
        return jsonify(medicos)
    
    def cadastrar_medico(self):
        return jsonify(self.__service.cadastrar_medico())
