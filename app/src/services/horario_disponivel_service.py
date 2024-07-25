
from src.database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from src.exception.CustomException import EntityNotFoundException


class HorarioDisponivelService():

    def __init__(self, horario_disponivel_repository: HorarioDisponivelRepository) -> None:
        self.__repository = horario_disponivel_repository


    def get_por_id(self, id):
        horario = self.__repository.get_horario_by_id(id)

        if not horario:
            raise EntityNotFoundException("Schedule not found")
        
        return horario
