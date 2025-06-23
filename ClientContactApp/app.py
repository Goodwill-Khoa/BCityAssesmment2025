from flask import Flask, render_template
from models import db
from routes import register_blueprints
from flask_login import LoginManager
from models.user import User
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    def jinja2_attribute(obj, name):
        return getattr(obj, name, "")

    app.jinja_env.filters['attribute'] = jinja2_attribute
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-very-secure-secret'

    db.init_app(app)
    register_blueprints(app)  # Register your main app blueprints
    # app.register_blueprint(admin_bp)  # Register the admin blueprint

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        # Create a default admin user if it doesn't exist
        if not User.query.filter_by(username='Admin').first():
            admin = User(username='Admin', is_superuser=True)
            admin.set_password('Admin')
            db.session.add(admin)
            db.session.commit()

    # Basic routes for template rendering
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
    
    @app.template_filter('getattr')
    def jinja_getattr(obj, attr):
        return getattr(obj, attr, '')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)