from .client import client_bp
from .contact import contact_bp

# You could also define a function to register blueprints:
def register_blueprints(app):
    app.register_blueprint(client_bp)
    app.register_blueprint(contact_bp)