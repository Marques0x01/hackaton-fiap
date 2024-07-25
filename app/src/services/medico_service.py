from src.database.repositories.medico_repository import MedicoRepository
from src.database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from src.models.mappers.medico_mapper import medico_to_dto
from src.utils.datetime_utils import time_to_string
from src.exception.CustomException import EntityNotFoundException, AlreadExistsException

class MedicoService:

    def __init__(self, 
                 medico_repository: MedicoRepository,
                 horario_disponivel_repository: HorarioDisponivelRepository) -> None:
        self.__medico_repository = medico_repository
        self.__horario_disponivel_repository = horario_disponivel_repository

    def list_all_doctors(self):
        try:
            doctors = self.__medico_repository.find_all_doctors()
            return [medico_to_dto(doctor).__dict__ for doctor in doctors]
        except Exception as e:
            print(f"An error occurred while listing all doctors: {e}")
            raise RuntimeError("Ocorreu um erro ao listar todos os médicos.") from e
    
    def list_doctors_by_speciality_and_state(self, specialty: str, state: str):
        try:
            doctors = self.__medico_repository.find_by_specialty_and_state(specialty, state)
            if not doctors:
                raise EntityNotFoundException(f'nenhum médico encontrado no estado {state} ou pela especialidade {specialty}')
            return [medico_to_dto(doctor).__dict__ for doctor in doctors]
        except EntityNotFoundException as e:
            raise e
        except Exception as e:
            print(f"An error occurred while listing doctors by specialty and state: {e}")
            raise RuntimeError("Ocorreu um erro ao listar médicos por especialidade e estado.") from e

    def create_doctor(self, payload):
        try:
            crm = payload.get('doctor').get('crm')
            medico = self.__medico_repository.find_doctor_by_crm(crm)
            if medico:
                raise AlreadExistsException(f'Médico já cadastrado com o CRM: {crm}')
            return self.__medico_repository.insert_doctor(payload)
        except AlreadExistsException as e:
            raise e
        except Exception as e:
            print(f"An error occurred while creating doctor: {e}")
            raise RuntimeError("Ocorreu um erro ao criar o médico.") from e
    
    def criar_horario_disponivel(self, payload: dict, crm: str):
        try:
            medico = self.__medico_repository.find_doctor_by_crm(crm)
            if medico is None:
                raise EntityNotFoundException(f'Médico com CRM {crm} não encontrado')
            payload['medico_id'] = medico.medico_id
            result = self.__horario_disponivel_repository.create_horario_disponivel(**payload)
            return {'message': 'Horário de atendimento inserido com sucesso', 'id_transacao': result.horario_id}
        except EntityNotFoundException as e:
            raise e
        except Exception as e:
            print(f"An error occurred while creating available schedule: {e}")
            raise RuntimeError("Ocorreu um erro ao criar o horário disponível.") from e
    
    def atualizar_horario_disponivel(self, payload: dict, crm: str, horario_id: int):
        try:
            medico = self.__medico_repository.find_doctor_by_crm(crm)
            if medico is None:
                raise EntityNotFoundException(f'Médico com CRM {crm} não encontrado')
            
            horario_encontrado = self.__horario_disponivel_repository.get_horario_disponivel_by_medico_id_and_horario_id(
                medico.medico_id, horario_id
            )
            if horario_encontrado is None:
                raise EntityNotFoundException('Horário não encontrado')
            horario_encontrado.hora_inicio = payload.get('hora_inicio')
            horario_encontrado.hora_fim = payload.get('hora_fim')
            horario_atualizado = self.__horario_disponivel_repository.update_horario_disponivel(horario_encontrado)
            print(horario_atualizado)
            return {
                'message': 'Horário atualizado com sucesso',
                'id': horario_id,
                'data': horario_atualizado.data,
                'novo_horario': {
                    'hora_inicio': time_to_string(horario_atualizado.hora_inicio),
                    'hora_fim': time_to_string(horario_atualizado.hora_fim)
                }
            }
        except Exception as e:
            print(f"An error occurred while updating available schedule: {e}")
            raise RuntimeError("Ocorreu um erro ao atualizar o horário disponível.") from e
    
    def listar_horarios_por_medico(self, crm: str):
        try:
            medico = self.__medico_repository.find_doctor_by_crm(crm)
            if medico is None:
                return {'message': f'Médico com CRM {crm} não encontrado'}
            
            horarios = self.__horario_disponivel_repository.get_horario_disponivel_by_medico_id(medico.medico_id)
            if not horarios:
                return {'message': f'Nenhum horário disponível para o Dr(a) {medico.nome}'}
            
            return [horario.to_dict() for horario in horarios]
        except Exception as e:
            print(f"An error occurred while listing schedules for doctor: {e}")
            raise RuntimeError("Ocorreu um erro ao listar os horários do médico.") from e

    def listar_medicos(self):
        try:
            return self.__medico_repository.find_all_doctors()
        except Exception as e:
            print(f"An error occurred while listing doctors: {e}")
            raise RuntimeError("Ocorreu um erro ao listar os médicos.") from e

    def cadastrar_medico(self, data):
        try:
            return self.__medico_repository.insert_doctor(data)
        except Exception as e:
            print(f"An error occurred while registering doctor: {e}")
            raise RuntimeError("Ocorreu um erro ao cadastrar o médico.") from e
