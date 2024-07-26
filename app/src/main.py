from flask import Flask

from src.routes.medico_route import medico_bp
from src.routes.agenda_route import agenda_bp
from src.routes.auth_route import auth_bp
from src.routes.paciente_route import paciente_bp
from src.routes.health_check_route import health_check_blueprint

app = Flask(__name__)

app.register_blueprint(health_check_blueprint, url_prefix='/health')
app.register_blueprint(medico_bp, url_prefix='/medicos')
app.register_blueprint(agenda_bp, url_prefix='/agenda')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(paciente_bp, url_prefix='/pacientes')

if __name__ == '__main__':
    app.run(debug=True)
