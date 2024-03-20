from flask import Flask
from flask_cors import CORS
from tournoi_routes import tournois_bp

app = Flask(__name__)
CORS(app, origins='http://localhost:4200')

app.register_blueprint(tournois_bp, url_prefix='/tournois')

if __name__ == '__main__':
    app.run(debug=True)
