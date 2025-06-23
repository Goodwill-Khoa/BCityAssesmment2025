from .client import client_bp
from .contact import contact_bp

# You could also define a function to register blueprints: This is for cleaner code
def register_blueprints(app):
    app.register_blueprint(client_bp)
    app.register_blueprint(contact_bp)

        # Import and register auth and admin blueprints
    from .auth import auth_bp
    from .admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)