from flask import Blueprint

from src.controllers.auth_controller import AuthController
from src.database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from src.database.repositories.medico_repository import MedicoRepository
from src.database.repositories.paciente_repository import PacienteRepository
from src.services.cognito_service import CognitoService
from src.services.medico_service import MedicoService
from src.services.paciente_service import PacienteService


service = CognitoService()
medico_service = MedicoService(MedicoRepository(), HorarioDisponivelRepository())
paciente_service = PacienteService(PacienteRepository())
controller = AuthController(service, medico_service, paciente_service)

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])(controller.login)
auth_bp.route('/register', methods=['POST'])(controller.register)