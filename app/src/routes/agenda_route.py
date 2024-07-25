from flask import Blueprint

from src.database.repositories.agendamento_repository import AgendamentoRepository
from src.database.repositories.paciente_repository import PacienteRepository
from src.database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from src.services.agendamento_service import AgendamentoService
from src.services.horario_disponivel_service import HorarioDisponivelService
from src.services.paciente_service import PacienteService
from src.controllers.agendamento_controller import AgendamentoController


paciente_repository = PacienteRepository()
agenda_repository = AgendamentoRepository()
horario_disponivel_repository = HorarioDisponivelRepository()

paciente_service = PacienteService(paciente_repository)
horario_disponivel_service = HorarioDisponivelService(horario_disponivel_repository)

service = AgendamentoService(agenda_repository, paciente_service, horario_disponivel_service)
controller = AgendamentoController(service)

agenda_bp = Blueprint('agenda', __name__)

agenda_bp.route('/', methods=['PATCH'])(controller.update_status_agenda)
agenda_bp.route('/', methods=['POST'])(controller.create_agenda)