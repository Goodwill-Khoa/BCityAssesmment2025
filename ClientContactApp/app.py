from flask import Flask
from models import db
from routes.client import client_bp
from routes.contact import contact_bp
from flask import render_template
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Only register blueprints ONCE!
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/clients_list')
    def clients():
        return render_template('client_list.html')

    @app.route('/client_form')
    def client_form():
        return render_template('client_form.html')

    @app.route('/client_detail')
    def client_detail():
        return render_template('client_detail.html')
    
    @app.route('/contact_list')
    def contact_list():
        return render_template('contact_list.html')
    
    @app.route('/contact_form')
    def contact_form():
        return render_template('contact_form.html')
    
    @app.route('/linked_clients')
    def linked_clients():
        return render_template('linked_clients.html')
    
    @app.route('/contact_detail')
    def contact_detail():
        return render_template('contact_detail.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)