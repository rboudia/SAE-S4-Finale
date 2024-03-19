from flask import Flask

from tournoi_routes import tournois_bp

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world"

app.register_blueprint(tournois_bp, url_prefix='/tournois')

if __name__ == '__main__':
    app.run(debug=True)