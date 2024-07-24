from flask import Blueprint

from src.database.repositories.agenda_repository import AgendaRepository
from src.database.repositories.paciente_repository import PacienteRepository
from src.database.repositories.horario_disponiel_repository import HorarioDisponivelRepository
from src.services.agenda_service import AgendaService
from src.services.horario_disponivel_service import HorarioDisponivelService
from src.services.paciente_service import PacienteService
from src.controllers.agenda_controller import AgendaController


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