from flask import Flask
from flask_cors import CORS
from tournoi_routes import tournois_bp
from joueur_routes import joueurs_bp
from equipement_routes import equipements_bp
from match_routes import matchs_bp

app = Flask(__name__)

# Routes registration
app.register_blueprint(tournois_bp, url_prefix='/api/tournois')
app.register_blueprint(joueurs_bp, url_prefix='/api/joueurs')
app.register_blueprint(equipements_bp, url_prefix='/api/equipements')
app.register_blueprint(matchs_bp, url_prefix='/api/matchs')

# CORS configuration
cors = CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
