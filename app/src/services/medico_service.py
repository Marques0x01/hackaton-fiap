from database.repositories.medico_repository import MedicoRepository


class MedicoService:

    def __init__(self, repository: MedicoRepository) -> None:
        self.__repository = repository

    def listar_medicos(self):
        return self.__repository.find_doctors()

    def cadastrar_medico(self, data):
        return self.__repository.create_doctor(data)
