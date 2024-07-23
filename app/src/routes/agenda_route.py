from flask import Blueprint

from database.repositories.agenda_repository import AgendaRepository
from database.repositories.paciente_repository import PacienteRepository
from database.repositories.horario_disponiel_repository import HorarioDisponivelRepository
from services.agenda_service import AgendaService
from services.horario_disponivel_service import HorarioDisponivelService
from services.paciente_service import PacienteService
from controllers.agenda_controller import AgendaController


paciente_repository = PacienteRepository()
agenda_repository = AgendaRepository()
horario_disponivel_repository = HorarioDisponivelRepository()

paciente_service = PacienteService(paciente_repository)
horario_disponivel_service = HorarioDisponivelService(horario_disponivel_repository)

service = AgendaService(agenda_repository, paciente_service, horario_disponivel_service)
controller = AgendaController(service)

agenda_bp = Blueprint('agenda', __name__)

agenda_bp.route('/', methods=['PATCH'])(controller.update_status_agenda)
agenda_bp.route('/', methods=['POST'])(controller.create_agenda)