from flask import Blueprint

from app.src.controllers.agenda_controller import AgendaController
from app.src.controllers.auth_controller import AuthController
from app.src.database.repositories.agenda_repository import AgendaRepository
from app.src.database.repositories.medico_repository import MedicoRepository
from app.src.database.repositories.paciente_repository import PacienteRepository
from app.src.services.agenda_service import AgendaService
from app.src.services.cognito_service import CognitoService
from app.src.services.horario_disponivel_service import HorarioDisponivelService
from app.src.services.medico_service import MedicoService
from app.src.services.paciente_service import PacienteService


service = CognitoService()
medico_service = MedicoService(MedicoRepository())
paciente_service = PacienteService(PacienteRepository())
controller = AuthController()

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])(controller.login)
auth_bp.route('/register', methods=['POST'])(controller.register)