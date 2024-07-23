from flask import Flask

from routes.medico_route import medico_bp
from routes.agenda_route import agenda_bp
from routes.auth_route import auth_bp
app = Flask(__name__)

app.register_blueprint(medico_bp, url_prefix='/medicos')
app.register_blueprint(agenda_bp, url_prefix='/agenda')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
