from flask import Flask

from routes.medico_route import medico_bp
app = Flask(__name__)

# POST /schedules -> doctor - Cadastro horário disponível medico LEO
# PATCH /schedules -> doctor - Atualiza horário disponível medico LEO
# GET /schedules -> doctor - Lista horários disponíveis LEO
# GET /doctors?especialidade=X -> paciente to doctor LEO OK
app.register_blueprint(medico_bp, url_prefix='/medicos')

if __name__ == '__main__':
    app.run(debug=True)
