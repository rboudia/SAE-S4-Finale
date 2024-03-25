from flask import Flask
from flask_cors import CORS
from tournoi_routes import tournois_bp
from joueur_routes import joueurs_bp
from equipement_routes import equipements_bp
from match_routes import matchs_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(tournois_bp, url_prefix='/tournois')
app.register_blueprint(joueurs_bp, url_prefix='/joueurs')
app.register_blueprint(equipements_bp, url_prefix='/equipements')
app.register_blueprint(matchs_bp, url_prefix='/matchs')

if __name__ == '__main__':
    app.run(debug=True)
