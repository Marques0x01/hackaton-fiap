from flask import request, jsonify
from src.services.medico_service import MedicoService

class MedicoController:

    def __init__(self, service: MedicoService) -> None:
        self.__service = service

    def get_all_doctors(self):
        doctors = self.__service.list_all_doctors()
        return jsonify(doctors)

    def get_doctors_por_especialidade_e_estado(self):
        especialidade = request.args.get('especialidade')
        estado = request.args.get('estado')
        medicos = self.__service.list_doctors_by_speciality_and_state(especialidade, estado)
        return jsonify(medicos)


    def post_doctor(self):
        data = request.get_json()
        print(data)
        return jsonify(self.__service.create_doctor(data))

    def get_horarios_disponiveis(self, crm: str): 
        horarios = self.__service.listar_horarios_por_medico(crm)
        return jsonify(horarios)

    def post_horario_disponivel(self, crm: str):
        data = request.get_json()
        return jsonify(self.__service.criar_horario_disponivel(data, crm))

    def patch_horario_disponivel(self, crm: str, horario_id: int):
        data = request.get_json()
        return jsonify(self.__service.atualizar_horario_disponivel(data, crm, horario_id))
