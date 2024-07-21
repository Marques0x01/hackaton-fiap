from flask import Flask

from routes.medico_route import medico_bp
app = Flask(__name__)

app.register_blueprint(medico_bp, url_prefix='/medicos')

if __name__ == '__main__':
    app.run(debug=True)
