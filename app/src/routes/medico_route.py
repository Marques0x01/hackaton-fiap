from flask import Blueprint

from database.repositories.medico_repository import MedicoRepository
from services.medico_service import MedicoService
from controllers.medico_controller import MedicoController


repository = MedicoRepository()
service = MedicoService(repository)
controller = MedicoController(service)


medico_bp = Blueprint('medicos', __name__)


medico_bp.route('/', methods=['GET'])(controller.get_medicos)
medico_bp.route('/', methods=['POST'])(controller.cadastrar_medico)