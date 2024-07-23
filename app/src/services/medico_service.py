from database.repositories.medico_repository import MedicoRepository
from database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from models.mappers.medico_mapper import medico_to_dto
from utils.datetime_utils import time_to_string



class MedicoService:

    def __init__(self, 
                 medico_repository: MedicoRepository,
                 horario_disponivel_repository: HorarioDisponivelRepository) -> None:
        self.__medico_repository = medico_repository
        self.__horario_disponivel_repository = horario_disponivel_repository

    def list_all_doctors(self):
        doctors =  self.__medico_repository.find_all_doctors()
        result = [medico_to_dto(doctor).__dict__ for doctor in doctors]
        return result
    
    def list_doctors_by_speciality_and_state(self, specialty: str, state: str):
        doctors = self.__medico_repository.find_by_specialty_and_state(specialty, state)
        result = [medico_to_dto(doctor).__dict__ for doctor in doctors]
        return result
    
    def create_doctor(self, payload):
        return self.__medico_repository.insert_doctor(payload)
    
    def criar_horario_disponivel(self, payload: dict, crm: str):
        print(crm)
        medico = self.__medico_repository.find_doctor_by_crm(crm)
        payload['medico_id'] = medico.medico_id
        print(payload)
        result = self.__horario_disponivel_repository.create_horario_disponivel(**payload)
        return {'message': 'horário de antedimento inserido com sucesso', 'id_transacao': result.horario_id} 
    
    def atualizar_horario_disponivel(self, payload: dict, crm, horario_id: int):
        medico = self.__medico_repository.find_doctor_by_crm(crm)
        if medico is None:
            return {'message': f'médico não encontrado crm: {crm}'}
        horario_encontrado = self.__horario_disponivel_repository.get_horario_disponivel_by_medico_id_and_horario_id(
            medico.medico_id, horario_id)
        if horario_encontrado is None:
            return {'message': 'horário não encontrado'}
        horario_encontrado.hora_inicio = payload.get('hora_inicio')
        horario_encontrado.hora_fim = payload.get('hora_fim')
        horario_atualizado = self.__horario_disponivel_repository.update_horario_disponivel(horario_encontrado)
        return {'message': 'horário atualizado com sucesso',
                'id': horario_id,
                'data': horario_atualizado.data,
                'novo_horario': {
                    'hora_inicio': time_to_string(horario_atualizado.hora_inicio),
                    'hora_fim': time_to_string(horario_atualizado.hora_fim)
                }
            }
    
    def listar_horarios_por_medico(self, crm: str):
        medico = self.__medico_repository.find_doctor_by_crm(crm)
        if medico is None:
            return {'message': f'médico não encontrado crm: {crm}'}
        horarios = self.__horario_disponivel_repository.get_horario_disponivel_by_medico_id(medico.medico_id)
        return horarios
    def listar_medicos(self):
        return self.__medico_repository.find_all_doctors()

    def cadastrar_medico(self, data):
        return self.__medico_repository.insert_doctor(data)
