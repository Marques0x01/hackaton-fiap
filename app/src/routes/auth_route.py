from flask import Blueprint

from controllers.auth_controller import AuthController
from database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from database.repositories.medico_repository import MedicoRepository
from database.repositories.paciente_repository import PacienteRepository
from services.cognito_service import CognitoService
from services.medico_service import MedicoService
from services.paciente_service import PacienteService


service = CognitoService()
medico_service = MedicoService(MedicoRepository(), HorarioDisponivelRepository())
paciente_service = PacienteService(PacienteRepository())
controller = AuthController(service, medico_service, paciente_service)

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])(controller.login)
auth_bp.route('/register', methods=['POST'])(controller.register)