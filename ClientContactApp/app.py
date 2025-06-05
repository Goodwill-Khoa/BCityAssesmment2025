from flask import Flask
from models import db
from routes.client import client_bp
from routes.contact import contact_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(client_bp)
    app.register_blueprint(contact_bp)

    @app.route('/')
    def index():
        return "<h2>ClientContactApp is running!</h2>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)