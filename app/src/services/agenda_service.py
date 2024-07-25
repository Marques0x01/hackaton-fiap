
from src.database.repositories.agendamento_repository import AgendamentoRepository
from src.services.horario_disponivel_service import HorarioDisponivelService
from src.services.paciente_service import PacienteService
from src.exception.CustomException import EntityNotFoundException


class AgendaService:

    def __init__(self, agenda_repository: AgendamentoRepository, paciente_service: PacienteService, horario_disponivel_service: HorarioDisponivelService) -> None:
        self.__agenda_repository = agenda_repository
        self.__paciente_service = paciente_service
        self.__horario_disponivel_service = horario_disponivel_service

    def save_agenda(self, agenda_id, paciente_documento):
        paciente = self.__paciente_service.get_por_documento(paciente_documento)
        horario = self.__horario_disponivel_service.get_por_id(agenda_id)

        return self.__agenda_repository.create_agendamento(horario.horario_id, paciente.paciente_id, "PENDING").to_dict()

    def update_status_agenda(self, agenda_id, status):
        return self.__agenda_repository.update_status(agenda_id, status)


    def get_agenda_por_id(self, agenda_id):

        agenda = self.__agenda_repository.get_por_id(agenda_id)

        if not agenda:
            raise EntityNotFoundException("agenda not found")
        
        return agenda