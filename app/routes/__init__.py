# app/routes/__init__.py

def register_blueprints(app):
    """
    Centralized blueprint registration.
    Importing blueprints here avoids circular imports.
    """
    from .onboarding import onboarding_bp
    from .feedback import feedback_bp
    from .push import push_bp
    from .device_token import device_token_bp
    from .test_push import test_push_bp

    app.register_blueprint(onboarding_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(push_bp)
    app.register_blueprint(device_token_bp)
    app.register_blueprint(test_push_bp)
