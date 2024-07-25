from src.database.repositories.agendamento_repository import AgendamentoRepository
from src.services.horario_disponivel_service import HorarioDisponivelService
from src.services.paciente_service import PacienteService
from src.exception.CustomException import EntityNotFoundException

class AgendamentoService:

    def __init__(self, agenda_repository: AgendamentoRepository, paciente_service: PacienteService, horario_disponivel_service: HorarioDisponivelService) -> None:
        self.__agenda_repository = agenda_repository
        self.__paciente_service = paciente_service
        self.__horario_disponivel_service = horario_disponivel_service

    def save_agenda(self, horario_id: int, paciente_documento: str) -> dict:
        """Cria um novo agendamento e retorna seus detalhes em formato de dicionário."""
        try:
            paciente = self.__paciente_service.get_por_documento(paciente_documento)
            horario = self.__horario_disponivel_service.get_por_id(horario_id)

            novo_agendamento = self.__agenda_repository.create_agendamento(
                horario_id=horario.horario_id,
                paciente_id=paciente.paciente_id,
                status="PENDING"
            )
            return novo_agendamento.to_dict()
        except ValueError as e:
            raise ValueError(f"Erro ao criar agendamento: {e}")

    def update_status_agenda(self, agendamento_id: int, status: str) -> dict:
        """Atualiza o status do agendamento e retorna os detalhes atualizados em formato de dicionário."""
        try:
            agendamento = self.__agenda_repository.update_status(agendamento_id, status=status)
            return agendamento.to_dict()
        except ValueError as e:
            raise ValueError(f"Erro ao atualizar o status do agendamento: {e}")

    def get_agenda_por_id(self, agendamento_id: int) -> dict:
        """Obtém os detalhes do agendamento por ID e retorna em formato de dicionário."""
        try:
            agendamento = self.__agenda_repository.get_agendamento_by_id(agendamento_id)
            if not agendamento:
                raise EntityNotFoundException("Agendamento não encontrado.")
            return agendamento.to_dict()
        except EntityNotFoundException as e:
            raise EntityNotFoundException(f"Erro ao obter agendamento: {e}")
        except ValueError as e:
            raise ValueError(f"Erro ao obter agendamento: {e}")
