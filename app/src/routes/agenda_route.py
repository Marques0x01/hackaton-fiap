from flask import Blueprint

from app.src.controllers.agenda_controller import AgendaController
from app.src.database.repositories.agenda_repository import AgendaRepository
from app.src.services.agenda_service import AgendaService
from app.src.services.horario_disponivel_service import HorarioDisponivelService
from app.src.services.paciente_service import PacienteService

service = AgendaService(AgendaRepository(), PacienteService(), HorarioDisponivelService())
controller = AgendaController(service)

agenda_bp = Blueprint('agenda', __name__)

agenda_bp.route('/', methods=['PATCH'])(controller.update_status_agenda)
agenda_bp.route('/', methods=['POST'])(controller.create_agenda)