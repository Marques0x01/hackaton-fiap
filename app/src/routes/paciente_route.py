from flask import Blueprint

from src.database.repositories.paciente_repository import PacienteRepository
from src.services.paciente_service import PacienteService
from src.controllers.paciente_controller import PacienteController

repository = PacienteRepository()
service = PacienteService(repository)
controller = PacienteController(service)

paciente_bp = Blueprint('pacientes', __name__)

paciente_bp.route('/', methods=['POST'])(controller.post_paciente)
