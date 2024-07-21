# from flask import Blueprint
# from controllers.paciente_controller import PacienteController

# paciente_bp = Blueprint('pacientes', __name__)

# paciente_bp.route('/', methods=['POST'])(PacienteController.create_paciente)
# paciente_bp.route('/', methods=['GET'])(PacienteController.get_pacientes)
# paciente_bp.route('/<int:paciente_id>', methods=['GET'])(PacienteController.get_paciente)
# paciente_bp.route('/<int:paciente_id>', methods=['PUT'])(PacienteController.update_paciente)
# paciente_bp.route('/<int:paciente_id>', methods=['DELETE'])(PacienteController.delete_paciente)
