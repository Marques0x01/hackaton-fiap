from flask import Blueprint

from src.database.repositories.medico_repository import MedicoRepository
from src.database.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from src.services.medico_service import MedicoService
from src.controllers.medico_controller import MedicoController


medico_repository = MedicoRepository()
horario_repository = HorarioDisponivelRepository()
service = MedicoService(medico_repository, horario_repository)
controller = MedicoController(service)


medico_bp = Blueprint('medicos', __name__)


medico_bp.route('/', methods=['GET'])(controller.get_all_doctors)
medico_bp.route('/buscar', methods=['GET'])(controller.get_doctors_por_especialidade_e_estado)
medico_bp.route('/', methods=['POST'])(controller.post_doctor)
medico_bp.route('/<string:crm>/horarios', methods=['GET'])(controller.get_horarios_disponiveis)
medico_bp.route('/<string:crm>/horarios', methods=['POST'])(controller.post_horario_disponivel)
medico_bp.route('/<string:crm>/horarios/<int:horario_id>', methods=['PATCH'])(controller.patch_horario_disponivel)