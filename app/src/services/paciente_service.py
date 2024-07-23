
from database.repositories.paciente_repository import PacienteRepository
from exception.CustomException import EntityNotFoundException


class PacienteService():

    def __init__(self, paciente_repository: PacienteRepository) -> None:
        self.__repository = paciente_repository

    def cadastrar_paciente(self, data):
        self.__repository.save_paciente(data)

    def get_por_documento(self, documento):
        paciente = self.__repository.get_paciente_por_id(documento)

        if not paciente:
            raise EntityNotFoundException("Patient not found")
        
        return paciente

